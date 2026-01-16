from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(50), unique=True, nullable=True) 
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True) 
    price = Column(Float, nullable=False) 
    category = Column(String(100), nullable=True)
    image_url = Column(String(500), nullable=True) 
    is_expensive = Column(Boolean, default=False)