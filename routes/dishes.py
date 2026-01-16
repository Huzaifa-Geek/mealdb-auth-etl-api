from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from database import get_db
from models import Dish
from dependencies import get_current_user
from schemas import DishResponse
from fastapi import APIRouter, Depends, HTTPException, status
from services.meal_fetch import fetch_and_store_dishes
import schemas 


router = APIRouter(prefix="/dishes", tags=["Dishes"])

# Get Dishes 

@router.get("/", response_model=schemas.DishListResponse) 
def get_dishes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    print(f"DEBUG: User {current_user.name} is_admin status: {current_user.is_admin}")

    
    if current_user.is_admin:
        dishes = db.query(Dish).all()
        role = "admin"
    else:
        dishes = db.query(Dish).filter(Dish.is_expensive == False).all()
        role = "user"

    return {
        "role": role,
        "total": len(dishes),
        "dishes": dishes 
    }



@router.post("/fetch", status_code=status.HTTP_201_CREATED)
def trigger_fetch(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Admin-only endpoint to sync database with TheMealDB API.
    """
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only admins can sync the database."
        )
    
    try:
        fetch_and_store_dishes(db)
        return {"message": "Database sync successful!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Sync failed: {str(e)}"
        )
    
