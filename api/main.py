from fastapi import FastAPI, UploadFile, File
import pandas as pd
from src.classification import classify_reviews
from src.intelligence import generate_all_intelligence

app = FastAPI()

@app.post("/generate-intelligence")
def generate(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    df = classify_reviews(df)

    return generate_all_intelligence(df)
