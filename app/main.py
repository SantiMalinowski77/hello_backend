from fastapi import FastAPI
from app.db import test_connection

app = FastAPI(title="hello backend")

@app.get("/")
def root():
    return {"ok": True, "message": "API funcionando"}

@app.get("/health/db")
def health_db():
    test_connection()
    return {"ok": True, "message": "DB conectada"}
