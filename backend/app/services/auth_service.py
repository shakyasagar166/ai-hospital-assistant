from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.database.models import User
from app.database.schemas import UserRegister
from app.core.security import get_password_hash, verify_password


class AuthService:
    @staticmethod
    def register(db: Session, data: UserRegister) -> User:
        existing = db.query(User).filter(User.email == data.email.lower()).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address is already registered in the hospital portal"
            )

        user = User(
            email=data.email.lower(),
            hashed_password=get_password_hash(data.password),
            full_name=data.full_name,
            role=data.role or "patient",
            blood_group=data.blood_group or "O+",
            emergency_contact=data.emergency_contact,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User:
        user = db.query(User).filter(User.email == email.lower()).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid clinical portal email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Patient account has been deactivated"
            )
        return user
