from fastapi import FastAPI

app = FastAPI(title="hello backend")

@app.get("/")
def root():
    return {"ok": True, "message": "API funcionando"}
