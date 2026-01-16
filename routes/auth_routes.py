from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import User
from schemas import UserCreate, UserLogin, TokenResponse
from auth import get_password_hash, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])



# Register

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # 1. Check if user already exists
    existing_user = db.query(User).filter(
        User.name == user_data.name
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # 2. Create new user instance
    
    new_user = User(
        name=user_data.name,
        password=get_password_hash(user_data.password),
        is_admin=getattr(user_data, "is_admin", False) 
    )

    # 3. Save to database with error handling

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error. User might already exist."
        )

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "is_admin": new_user.is_admin
    }



# Login

@router.post("/login", response_model=TokenResponse)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.name == user_data.name
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    db_password = str(user.password)
    user_is_admin = bool(user.is_admin)

    if not verify_password(user_data.password, db_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        data={"user_id": user.id, "is_admin": user_is_admin}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "admin" if user_is_admin else "user"
    }