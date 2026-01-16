from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base, SessionLocal     
from routes import auth_routes, dishes
from services.meal_fetch import fetch_and_store_dishes
from database import engine, Base
import models 

Base.metadata.drop_all(bind=engine) 

Base.metadata.create_all(bind=engine)
print("Database tables recreated successfully!")

# Lifespan (Startup/Shutdown)

@asynccontextmanager
async def lifespan(app: FastAPI):
   
    print("Creating database tables")
    Base.metadata.create_all(bind=engine)

    
    print("Fetching dishes from Mealdb API")
    db = SessionLocal()
    try:
        fetch_and_store_dishes(db)
    finally:
        db.close()
    
    yield  
    print("Shutting down...")


# App Initialization

app = FastAPI(
    title="TheMealDB API",
    description="Role-based API for dishes (Admin / User)",
    version="1.0.0",
    lifespan=lifespan
)

# Routes

app.include_router(auth_routes.router)
app.include_router(dishes.router)


# Base.metadata.drop_all(bind=engine) 

Base.metadata.create_all(bind=engine)
print("Database tables recreated successfully!")
