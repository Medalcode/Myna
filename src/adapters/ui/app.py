import gradio as gr
import pandas as pd
from typing import List, Tuple, Any

# Imports from Core (Inside)
from src.core.models import AnalysisSession
from src.core.domain_services import StatisticalAnalyzer, DataCleaner, DataScaler, OutlierManager, Clusterer

# Imports from Adapters (Outside)
from src.adapters.fs.file_io import FileSystemAdapter
from src.adapters.visualization.plotter import PlottingAdapter

def create_app():
    """
    Constructs the Gradio App Blocks.
    """
    
    # --- HELPER FUNCTIONS (CONTROLLERS) ---
    
    def on_load_data(file_obj, delimiter, session: AnalysisSession):
        if session is None: session = AnalysisSession()
        
        df, error = FileSystemAdapter.load_file(file_obj, delimiter)
        if error:
            return session, f"Error: {error}", pd.DataFrame(), gr.update(choices=[]), gr.update(choices=[]), gr.update(choices=[]), gr.update(choices=[]), gr.update(choices=[]), gr.update(choices=[])
            
        session.current_df = df
        session.add_log(f"Carga: Archivo cargado. Dimensiones: {df.shape}")
        
        preview = df.head().round(3).fillna('-')
        msg = f"Carga Exitosa. Dimensiones: {df.shape}"
        
        # Update Choices
        numeric_cols = StatisticalAnalyzer.get_numeric_columns(df)
        all_cols = df.columns.tolist()
        
        return (
            session, 
            msg, 
            preview,
            gr.update(choices=all_cols), # Nulos
            gr.update(choices=numeric_cols), # Escalar
            gr.update(choices=numeric_cols), # Outliers
            gr.update(choices=numeric_cols), # Clustering Params
            gr.update(choices=numeric_cols), # Clustering X
            gr.update(choices=numeric_cols), # Clustering Y
            gr.update(choices=numeric_cols), # Distribucion
            gr.update(choices=numeric_cols), # Regresion X
            gr.update(choices=numeric_cols)  # Regresion Y
        )

    def on_clean_nulls(session: AnalysisSession, cols, method):
        if not session or session.current_df is None: return session, "Error: No hay datos.", pd.DataFrame()
        if not cols: return session, "Aviso: Seleccione columnas.", session.current_df.head()
        
        df_new, count = DataCleaner.handle_nulls(session.current_df, cols, method)
        session.current_df = df_new
        session.add_log(f"Limpieza Nulos: {count} valores tratados con {method} en {cols}.")
        
        return session, f"Se trataron {count} valores nulos.", df_new.head().round(3).fillna('-')

    def on_scale_data(session: AnalysisSession, cols, method):
        if not session or session.current_df is None: return session, "Error: No hay datos.", pd.DataFrame()
        if not cols: return session, "Aviso: Seleccione columnas.", session.current_df.head()
        
        df_new = DataScaler.apply_scaling(session.current_df, cols, method)
        session.current_df = df_new
        session.add_log(f"Escalado: {cols} escaladas con {method}.")
        
        return session, f"Escalado aplicado a {len(cols)} columnas.", df_new.head().round(3).fillna('-')

    def on_detect_outliers(session: AnalysisSession, col, method):
        if not session or session.current_df is None: return session, "Error: No hay datos.", pd.DataFrame()
        if not col: return session, "Aviso: Seleccione columna.", session.current_df.head()
        
        df_new, count, msg_detail = OutlierManager.detect_and_treat(session.current_df, col, method)
        session.current_df = df_new
        session.add_log(f"Outliers ({col}): {msg_detail} ({count} afectados).")
        
        return session, f"Resultado: {msg_detail}", df_new.head().round(3).fillna('-')

    def on_analyze_stats(session: AnalysisSession):
        if not session or session.current_df is None: return "No hay datos.", pd.DataFrame()
        
        analyzer = StatisticalAnalyzer()
        stats = analyzer.calculate_descriptive_stats(session.current_df)
        shape = analyzer.calculate_distribution_shape(session.current_df)
        corr = analyzer.calculate_correlation_matrix(session.current_df)
        
        # Format Text
        md_text = "### Estadísticas Descriptivas\n" + stats.to_markdown() + "\n\n### Forma (Curtosis/Asimetría)\n" + shape.to_markdown()
        
        return md_text, corr.round(3).fillna('-')

    def on_generate_plots(session: AnalysisSession, col_dist, col_reg_x, col_reg_y):
        if not session or session.current_df is None: return None, None, None, "No hay datos."
        
        p_corr = PlottingAdapter.plot_correlation_heatmap(session.current_df)
        p_dist = PlottingAdapter.plot_distribution(session.current_df, col_dist)
        p_reg = PlottingAdapter.plot_regression(session.current_df, col_reg_x, col_reg_y)
        
        return p_corr, p_dist, p_reg, "Gráficos Generados."

    def on_run_clustering(session: AnalysisSession, cols, k, x_plot, y_plot):
        if not session or session.current_df is None: return None, None, "No hay datos."
        if not cols or len(cols) < 2: return None, None, "Seleccione al menos 2 variables."
        
        df_new, msg = Clusterer.kmeans(session.current_df, cols, k)
        session.current_df = df_new
        session.add_log(f"Clustering: {msg}")
        
        # Auto-plot result if x and y selected
        fig = None
        if x_plot and y_plot:
            fig = PlottingAdapter.plot_clusters(df_new, x_plot, y_plot)
            
        return df_new.head().round(3).fillna('-'), fig, msg

    def on_export(session: AnalysisSession, fmt):
        if not session or session.current_df is None: return "No hay datos.", None, None
        
        file_path, err = FileSystemAdapter.export_file(session.current_df, fmt)
        log_path = FileSystemAdapter.save_report(session.get_logs_as_string())
        
        if err: return f"Error: {err}", None, None
        return "Archivos listos.", file_path, log_path
        

    # --- UI LAYOUT ---
    
    with gr.Blocks(title="HMS: Hermes Data Mining") as app:
        gr.Markdown("## 💎 Hermes: Minería de Datos Modular")
        
        # State
        session_state = gr.State(AnalysisSession())
        
        with gr.Tab("1. Carga"):
            with gr.Row():
                f_input = gr.File(label="Archivo (CSV/Excel)")
                radio_sep = gr.Radio(["Coma (,)", "Punto y Coma (;)"], value="Coma (,)", label="Separador")
                btn_load = gr.Button("Cargar", variant="primary")
            
            txt_status = gr.Textbox(label="Estado")
            df_preview = gr.Dataframe(label="Vista Previa", interactive=False)

        with gr.Tab("2. Limpieza"):
            gr.Markdown("### Nulos")
            with gr.Row():
                dd_null_cols = gr.Dropdown(label="Columnas", multiselect=True)
                radio_null_method = gr.Radio(["Eliminar filas", "Llenar con promedio", "Llenar con mediana (Mejora 5)", "Llenar con moda (Categórica)", "Llenar con cero"], label="Método")
                btn_null = gr.Button("Aplicar")
            txt_null_res = gr.Textbox(label="Resultado")

            gr.Markdown("### Escalado")
            with gr.Row():
                dd_scale_cols = gr.Dropdown(label="Columnas Numéricas", multiselect=True)
                radio_scale_method = gr.Radio(["Min-Max", "Z-Score"], label="Método")
                btn_scale = gr.Button("Aplicar")
            txt_scale_res = gr.Textbox(label="Resultado")

        with gr.Tab("3. Outliers"):
            with gr.Row():
                dd_outlier_col = gr.Dropdown(label="Columna (Numérica)")
                radio_outlier_method = gr.Radio(["Informar", "Eliminar registros", "Capping (Winsorización)"], label="Tratamiento")
                btn_outlier = gr.Button("Detectar/Tratar")
            txt_outlier_res = gr.Textbox(label="Resultado")

        with gr.Tab("4. Análisis"):
            btn_analyze = gr.Button("Ejecutar Análisis")
            md_results = gr.Markdown(label="Resultados")
            df_corr = gr.Dataframe(label="Matriz Correlación")

        with gr.Tab("5. Clustering (K-Means)"):
            gr.Markdown("### Agrupamiento No Supervisado")
            with gr.Row():
                dd_cluster_features = gr.Dropdown(label="Variables para Clustering", multiselect=True)
                slider_k = gr.Slider(minimum=2, maximum=10, step=1, label="Número de Clusters (K)", value=3)
                btn_cluster = gr.Button("Ejecutar Clustering")
            
            with gr.Row():
                dd_clus_x = gr.Dropdown(label="Eje X (Visualización)")
                dd_clus_y = gr.Dropdown(label="Eje Y (Visualización)")
            
            txt_clus_res = gr.Textbox(label="Estado")
            df_clus_preview = gr.Dataframe(label="Vista Previa (con Cluster)")
            plot_cluster = gr.Plot(label="Visualización de Clusters")

        with gr.Tab("6. Visualización"):
            with gr.Row():
                dd_plot_dist = gr.Dropdown(label="Columna Distribución")
                dd_plot_x = gr.Dropdown(label="Eje X")
                dd_plot_y = gr.Dropdown(label="Eje Y")
                btn_plot = gr.Button("Generar Gráficos Interactivos")
            
            with gr.Row():
                # IMPROVEMENT: Using gr.Plot instead of gr.Image
                plot_corr = gr.Plot(label="Correlación")
            
            with gr.Row():
                plot_dist = gr.Plot(label="Distribución")
                plot_reg = gr.Plot(label="Regresión")
                
            txt_plot_status = gr.Textbox(label="Estado Gráficos")

        with gr.Tab("7. Exportar"):
            radio_fmt = gr.Radio(["CSV", "Excel"], label="Formato", value="CSV")
            btn_export = gr.Button("Descargar")
            with gr.Row():
                f_out_data = gr.File(label="Datos")
                f_out_log = gr.File(label="Log")

        # --- BINDINGS ---
        
        # Load
        btn_load.click(
            on_load_data,
            inputs=[f_input, radio_sep, session_state],
            outputs=[session_state, txt_status, df_preview, dd_null_cols, dd_scale_cols, dd_outlier_col, dd_cluster_features, dd_clus_x, dd_clus_y, dd_plot_dist, dd_plot_x, dd_plot_y]
        )
        
        # Clean
        btn_null.click(on_clean_nulls, inputs=[session_state, dd_null_cols, radio_null_method], outputs=[session_state, txt_null_res, df_preview])
        btn_scale.click(on_scale_data, inputs=[session_state, dd_scale_cols, radio_scale_method], outputs=[session_state, txt_scale_res, df_preview])
        
        # Outlier
        btn_outlier.click(on_detect_outliers, inputs=[session_state, dd_outlier_col, radio_outlier_method], outputs=[session_state, txt_outlier_res, df_preview])
        
        # Analyze
        btn_analyze.click(on_analyze_stats, inputs=[session_state], outputs=[md_results, df_corr])
        
        # Cluster
        btn_cluster.click(on_run_clustering, inputs=[session_state, dd_cluster_features, slider_k, dd_clus_x, dd_clus_y], outputs=[df_clus_preview, plot_cluster, txt_clus_res])

        # Plot (Updated outputs for gr.Plot)
        btn_plot.click(on_generate_plots, inputs=[session_state, dd_plot_dist, dd_plot_x, dd_plot_y], outputs=[plot_corr, plot_dist, plot_reg, txt_plot_status])
        
        # Export
        btn_export.click(on_export, inputs=[session_state, radio_fmt], outputs=[txt_status, f_out_data, f_out_log])

    return app
