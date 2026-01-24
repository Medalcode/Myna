from fastapi import FastAPI, UploadFile, File, Form, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
import pandas as pd
import io
import json
from typing import List, Optional

# Core & Adapters
from src.core.models import AnalysisSession
from src.core.domain_services import StatisticalAnalyzer, DataCleaner, DataScaler, Clusterer
from src.adapters.fs.file_io import FileSystemAdapter
from src.adapters.visualization.plotter import PlottingAdapter

app = FastAPI(title="Myna API")

# Mount Static & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global Session (Single User Mode)
session = AnalysisSession()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), delimiter: str = Form(",")):
    contents = await file.read()
    # Create a BytesIO object to mimic file-like object for pandas
    file_obj = io.BytesIO(contents)
    file_obj.name = file.filename # Adapter expects .name attribute
    
    df, error = FileSystemAdapter.load_file(file_obj, delimiter)
    
    if error:
        return JSONResponse(status_code=400, content={"error": error})
        
    session.current_df = df
    session.add_log(f"API: Uploaded {file.filename}")
    
    cols = df.columns.tolist()
    num_cols = StatisticalAnalyzer.get_numeric_columns(df)
    
    preview = df.head(10).fillna("").to_dict(orient="records")
    
    return {
        "message": "Carga exitosa", 
        "columns": cols, 
        "numeric_columns": num_cols,
        "preview": preview,
        "shape": df.shape
    }

@app.post("/api/clean/nulls")
async def clean_nulls(cols: List[str] = Form(...), method: str = Form(...)):
    if session.current_df is None: return JSONResponse(status_code=400, content={"error": "No dataframe"})
    
    # cols comes as a list of strings from form, might need parsing depending on how JS sends it
    # If sent as same key multiple times: cols=A&cols=B
    
    df_new, count = DataCleaner.handle_nulls(session.current_df, cols, method)
    session.current_df = df_new
    session.add_log(f"API: Nulls cleaned with {method} on {cols}")
    
    return {"message": f"Se trataron {count} valores.", "preview": df_new.head(10).fillna("").to_dict(orient="records")}

@app.post("/api/clean/scale")
async def scale_data(cols: List[str] = Form(...), method: str = Form(...)):
    if session.current_df is None: return JSONResponse(status_code=400, content={"error": "No dataframe"})
    
    df_new = DataScaler.apply_scaling(session.current_df, cols, method)
    session.current_df = df_new
    session.add_log(f"API: Scaled {cols} with {method}")
    
    return {"message": f"Escalado completado.", "preview": df_new.head(10).fillna("").to_dict(orient="records")}

@app.get("/api/stats")
async def get_stats():
    if session.current_df is None: return JSONResponse(status_code=400, content={"error": "No dataframe"})
    
    analyzer = StatisticalAnalyzer()
    desc = analyzer.calculate_descriptive_stats(session.current_df)
    corr = analyzer.calculate_correlation_matrix(session.current_df)
    
    return {
        "descriptive": desc.to_markdown() if not desc.empty else "No data",
        "correlation": corr.to_json(orient="split") if corr is not None else None
    }

@app.post("/api/cluster")
async def run_cluster(cols: List[str] = Form(...), k: int = Form(...)):
    if session.current_df is None: return JSONResponse(status_code=400, content={"error": "No dataframe"})
    
    df_new, msg = Clusterer.kmeans(session.current_df, cols, k)
    session.current_df = df_new
    
    return {
        "message": msg,
        "preview": df_new.head(10).fillna("").to_dict(orient="records")
    }

@app.post("/api/plot")
async def get_plot(
    type: str = Form(...), 
    x: str = Form(None), 
    y: str = Form(None), 
    col: str = Form(None)
):
    if session.current_df is None: return JSONResponse(status_code=400, content={"error": "No dataframe"})
    
    fig = None
    if type == "correlation":
        fig = PlottingAdapter.plot_correlation_heatmap(session.current_df)
    elif type == "distribution":
        fig = PlottingAdapter.plot_distribution(session.current_df, col)
    elif type == "regression":
        fig = PlottingAdapter.plot_regression(session.current_df, x, y)
    elif type == "cluster":
        # Assumes 'Cluster' col exists
        fig = PlottingAdapter.plot_clusters(session.current_df, x, y)
        
    if fig:
        return json.loads(fig.to_json())
    return {"error": "Could not generate plot"}
