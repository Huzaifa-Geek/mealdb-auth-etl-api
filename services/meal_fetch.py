import requests
import random
from sqlalchemy.orm import Session
from models import Dish

# Using TheMealDB (Public API)

API_URL = "https://www.themealdb.com/api/json/v1/1/search.php?s="

def fetch_and_store_dishes(db: Session):
    try:
      
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()

        meals = data.get("meals", [])
        if not meals:
            print("No meals found in the API response")
            return

        added_count = 0
        
        for meal in meals:
            dish_name = meal.get("strMeal")
            external_id = meal.get("idMeal")
            category = meal.get("strCategory")
            description = meal.get("strInstructions")
            image_url = meal.get("strMealThumb")

           
            price = round(random.uniform(500, 2500), 2)

            
            existing_dish = db.query(Dish).filter(Dish.external_id == external_id).first()
            
            if not existing_dish:
                new_dish = Dish(
                    name=dish_name,
                    external_id=external_id,
                    description=description[:500] if description else "", 
                    price=price,
                    category=category,
                    image_url=image_url,
                    is_expensive=price > 1500
                )
                db.add(new_dish)
                added_count += 1
                print(f"Adding: {dish_name} Rs. {price}")

        # 4. Save to Database
        
        db.commit()
        print(f"Process Complete Added {added_count} new dishes from TheMealDB")

    except Exception as e:
        db.rollback()
        print(f"Error fetching dishes: {e}")