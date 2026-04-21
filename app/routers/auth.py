from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib

from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

router = APIRouter()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"ok": True, "message": "Usuario creado", "user_id": new_user.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if existing_user.password_hash != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {
        "ok": True,
        "message": "Login correcto",
        "token": f"user-{existing_user.id}"
    }
