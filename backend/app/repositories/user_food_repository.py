from datetime import datetime

from sqlalchemy import extract
from app.models import UserFoodPreferences, UserFood, FoodItem


class UserFoodRepository:
    def __init__(self, db):
        self.db = db

    def adjust_shelf_life(self, user_id, food_id, shelf_life):
        preference = (
            self.db.session.query(UserFoodPreferences)
            .filter_by(user_id=user_id, food_item_id=food_id)
            .first()
        )
        if preference:
            preference.shelf_life = shelf_life
        else:
            new_preference = UserFoodPreferences(
                user_id=user_id, food_item_id=food_id, shelf_life=shelf_life
            )
            print(f"Added new preference: {new_preference}")
            self.db.session.add(new_preference)

    def add_user_food(self, user_id, food_id, expiration_date):
        user_food = UserFood(
            user_id=user_id, food_item_id=food_id, expiration_date=expiration_date
        )
        self.db.session.add(user_food)

    def get_user_foods(self, user_id):
        current_month = datetime.now().month
        current_year = datetime.now().year
        user_foods = (
            self.db.session.query(UserFood)
            .filter_by(user_id=user_id)
            .filter(
                extract("month", UserFood.expiration_date) == current_month,
                extract("year", UserFood.expiration_date) == current_year,
            )
            .all()
        )
        return [
            {
                "food_name": uf.food_item.name,
                "expiration_date": uf.expiration_date.isoformat(),
            }
            for uf in user_foods
        ]
