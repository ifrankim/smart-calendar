from app.models import FoodItem, UserFoodPreferences


class FoodServiceRepository:
    def __init__(self, db):
        self.db = db

    def get_or_create_food_item(self, food_name, shelf_life):
        existing_food = (
            self.db.session.query(FoodItem).filter_by(name=food_name).first()
        )
        if not existing_food:
            new_food = FoodItem(name=food_name, shelf_life=shelf_life)
            self.db.session.add(new_food)
            self.db.session.commit()
            print(f"Added new food to database: {food_name}")
            return new_food
        return existing_food

    def get_user_shelf_life(self, user_id, food_id):
        user_preference = (
            self.db.session.query(UserFoodPreferences)
            .filter_by(user_id=user_id, food_item_id=food_id)
            .first()
        )
        if user_preference:
            return user_preference.shelf_life
        return None
