import pandas as pd
from pathlib import Path
from typing import Union, Tuple
import io

class FileSystemAdapter:
    """
    Driven Adapter for File I/O.
    Shields the Core from file format details and path handling.
    """
    
    @staticmethod
    def load_file(file_obj, delimiter: str = ",") -> Tuple[pd.DataFrame, str]:
        """
        Loads a file (CSV or Excel) into a DataFrame.
        Returns (DataFrame, ErrorMessage).
        """
        if file_obj is None:
            return None, "Error: Debe subir un archivo."

        # Gradio passes a named temp file path usually, or a file-like object
        # In newer Gradio versions, it might be an object with .name
        path_str = getattr(file_obj, 'name', str(file_obj))
        path = Path(path_str)
        
        try:
            df = None
            if path.suffix.lower() == '.csv':
                # Try UTF-8 first, then ISO-8859-1
                try:
                    df = pd.read_csv(path, delimiter=delimiter, encoding="utf-8")
                except UnicodeDecodeError:
                    df = pd.read_csv(path, delimiter=delimiter, encoding="ISO-8859-1")
                
                if df.shape[1] == 1:
                     return None, "Error: CSV de una sola columna. Verifique el delimitador."

            elif path.suffix.lower() in ['.xls', '.xlsx']:
                df = pd.read_excel(path)
            else:
                return None, "Error: Formato no soportado (use CSV o Excel)."
                
            # Basic sanitization
            df.replace([float('inf'), float('-inf')], float('nan'), inplace=True)
            return df, ""
            
        except Exception as e:
            return None, f"Error de lectura: {str(e)}"

    @staticmethod
    def export_file(df: pd.DataFrame, format_type: str) -> Tuple[str, str]:
        """
        Saves DataFrame to disk.
        Returns (file_path, error_message).
        """
        if df is None:
            return None, "No hay datos para exportar."
            
        try:
            if format_type == "CSV":
                filename = "datos_procesados.csv"
                df.to_csv(filename, index=False)
                return filename, ""
            elif format_type == "Excel":
                filename = "datos_procesados.xlsx"
                df.to_excel(filename, index=False)
                return filename, ""
            else:
                return None, "Formato desconocido."
        except Exception as e:
            return None, str(e)

    @staticmethod
    def save_report(logs: str, filename: str = "reporte_analisis.txt") -> str:
        with open(filename, "w") as f:
            f.write(logs)
        return filename
