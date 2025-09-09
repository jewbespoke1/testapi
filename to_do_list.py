from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
from pathlib import Path
import io
import uuid

app = FastAPI(title="To-Do List API", version="0.2.0")


def generate_to_do_list_from_df(
    df: pd.DataFrame,
    weight_qty=0.72,
    weight_age=0.28,
    top_n=15,
):
    df.columns = df.columns.str.strip()

    if "Qty(Kgs)" not in df.columns:
        raise ValueError("Missing 'Qty(Kgs)' column in input file")
    if "Age" not in df.columns:
        df["Age"] = 0

    df["Age"] = pd.to_numeric(df["Age"], errors="coerce").fillna(0).astype(int)
    df["Qty(Kgs)"] = pd.to_numeric(df["Qty(Kgs)"], errors="coerce").fillna(0.0)

    def safe_norm(series):
        if series.max() == series.min():
            return pd.Series([0.5] * len(series), index=series.index)
        return (series - series.min()) / (series.max() - series.min())

    df["Qty_norm"] = safe_norm(df["Qty(Kgs)"])
    df["Age_norm"] = safe_norm(df["Age"])
    df["Score"] = df["Qty_norm"] * weight_qty + df["Age_norm"] * weight_age

    df = df.sort_values("Score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1

    keep_cols = [
        "Rank", "BTQ", "Doc Type", "Area", "Process Stage",
        "Doc No", "Doc Date", "Qty(Kgs)", "Age"
    ]
    keep_cols = [c for c in keep_cols if c in df.columns]
    top_items = df.head(top_n)[keep_cols]

    return top_items


@app.post("/to_do_list/json")
async def create_to_do_list_json(file: UploadFile = File(...)):
    """
    Upload CSV, generate to-do list JSON file, and return the JSON response.
    """
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    try:
        top_items = generate_to_do_list_from_df(df)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

    # Save JSON file on server with unique name
    outdir = Path("outputs")
    outdir.mkdir(exist_ok=True)
    file_id = uuid.uuid4().hex
    json_path = outdir / f"to_do_list_{file_id}.json"
    top_items.to_json(json_path, orient="records", indent=2)

    return FileResponse(json_path, media_type="application/json", filename="to_do_list.json")
