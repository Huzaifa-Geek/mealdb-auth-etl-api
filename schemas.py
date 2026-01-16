from pydantic import BaseModel
from typing import Optional, List

# USER SCHEMAS 

class UserCreate(BaseModel):
    name: str
    password: str
    is_admin: bool = False

class UserLogin(BaseModel):
    name: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    is_admin: bool

    class Config:
        from_attributes = True

# AUTH SCHEMAS

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str

# DISH SCHEMAS 


class DishBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    image_url: Optional[str] = None  
    external_id: Optional[str] = None

class DishCreate(DishBase):
    pass 

class DishResponse(DishBase):
    id: int
    is_expensive: bool

    class Config:
        from_attributes = True

class DishListResponse(BaseModel):
    role: str
    total: int
    dishes: List[DishResponse]