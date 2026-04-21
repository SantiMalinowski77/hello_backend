from fastapi import FastAPI
from app.db import engine
from app.models.user import User
from app.models.note import Note
from app.routers.auth import router as auth_router


app = FastAPI(title="hello backend")

User.metadata.create_all(bind=engine)
Note.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
def root():
    return {"ok": True, "message": "API funcionando"}

@app.get("/health/db")
def health_db():
    test_connection()
    return {"ok": True, "message": "DB conectada"}
