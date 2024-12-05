from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shelf_life = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))


class UserFood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey("food_item.id"), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)

    user = db.relationship("User", backref="user_food_items", lazy=True)
    food_item = db.relationship("FoodItem", backref="user_foods", lazy=True)


class UserFoodPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey("food_item.id"), nullable=False)
    shelf_life = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref="user_food_preferences", lazy=True)
    food_item = db.relationship("FoodItem", backref="user_food_preferences", lazy=True)
