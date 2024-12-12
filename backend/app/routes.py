from flask import Blueprint, request, jsonify
from app.models import User, FoodItem, UserFood, UserFoodPreferences
from app import db
from datetime import datetime, timedelta
from app.services import process_image
from app.repositories.user_food_repository import UserFoodRepository
from app.repositories.food_service_repository import FoodServiceRepository

routes = Blueprint("routes", __name__)


def validate_user(user_id):
    """Valida se o usuário existe no banco de dados."""
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} does not exist.")
    return user


def validate_food(food_id):
    """Valida se o item de comida existe no banco de dados."""
    food = FoodItem.query.get(food_id)
    if not food:
        raise ValueError(f"Food item with ID {food_id} does not exist.")
    return food


@routes.route("/scan_food", methods=["POST"])
def scan_food():
    try:
        print(request.form)
        user_id = request.form.get("user_id")
        if not user_id:
            raise ValueError("Missing user_id in request body.")

        if "image" not in request.files:
            raise ValueError("No image uploaded.")

        validate_user(user_id)

        image = request.files["image"]
        detected_food = process_image(image)
        if detected_food["food"] == "" or detected_food["shelf_life"] == "":
            return jsonify(detected_food)
        food_name = detected_food["food"].lower()

        repo = FoodServiceRepository(db)

        existing_food = repo.get_or_create_food_item(
            food_name, detected_food["shelf_life"]
        )
        print(existing_food)
        user_shelf_life = repo.get_user_shelf_life(user_id, existing_food.id)
        detected_food["shelf_life"] = (
            user_shelf_life if user_shelf_life else existing_food.shelf_life
        )

        detected_food["category"] = existing_food.category
        detected_food["food_item_id"] = existing_food.id

        return jsonify(detected_food)

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route("/adjust_user_shelf_life", methods=["POST"])
def adjust_user_shelf_life():
    try:
        data = request.json
        user_id = data["user_id"]
        food_id = data["food_id"]
        new_shelf_life = data["shelf_life"]

        validate_user(user_id)
        validate_food(food_id)

        repo = UserFoodRepository(db)
        repo.adjust_shelf_life(user_id, food_id, new_shelf_life)
        db.session.commit()
        return jsonify(
            {
                "message": "Shelf life ajustado com sucesso!",
                "shelf_life": new_shelf_life,
            }
        )
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route("/add_user_food", methods=["POST"])
def add_user_food():
    try:
        data = request.json
        user_id = data["user_id"]
        food_item_id = data["food_item_id"]

        validate_user(user_id)
        validate_food(food_item_id)

        preference = UserFoodPreferences.query.filter_by(
            user_id=user_id, food_id=food_item_id
        ).first()
        shelf_life = (
            preference.shelf_life
            if preference
            else FoodItem.query.get(food_item_id).default_shelf_life
        )

        expiration_date = datetime.now() + timedelta(days=shelf_life)

        user_food = UserFood(
            user_id=user_id, food_item_id=food_item_id, expiration_date=expiration_date
        )
        db.session.add(user_food)
        db.session.commit()

        return jsonify(
            {
                "message": f"Comida associada ao usuário com validade ajustada!",
                "expiration_date": expiration_date.date().isoformat(),
            }
        )
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route("/get_user_preferences/<int:user_id>", methods=["GET"])
def get_user_preferences(user_id):
    try:
        validate_user(user_id)
        preferences = UserFoodPreferences.query.filter_by(user_id=user_id).all()
        result = [
            {
                "food_id": pref.food_id,
                "food_name": FoodItem.query.get(pref.food_id).name,
                "shelf_life": pref.shelf_life,
            }
            for pref in preferences
        ]
        return jsonify(result)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route("/get_food_items", methods=["GET"])
def get_food_items():
    try:
        foods = FoodItem.query.all()
        result = [
            {
                "id": food.id,
                "name": food.name,
                "category": food.category,
                "shelf_life": food.shelf_life,
            }
            for food in foods
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route("/get_food_item_by_id/<int:food_item_id>", methods=["GET"])
def get_food_item_by_id(food_item_id):
    try:
        food_item = FoodItem.query.get(food_item_id)
        if not food_item:
            return jsonify({"error": "Food item not found"}), 404

        result = {
            "id": food_item.id,
            "name": food_item.name,
            "category": food_item.category,
            "shelf_life": food_item.shelf_life,
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route("/get_food_item_by_name", methods=["GET"])
def get_food_item_by_name():
    try:
        name = request.args.get("name")
        food_item = FoodItem.query.filter_by(name=name).first()
        if not food_item:
            return jsonify({"error": "Food item not found"}), 404

        result = {
            "id": food_item.id,
            "name": food_item.name,
            "category": food_item.category,
            "shelf_life": food_item.shelf_life,
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route("/get_user_foods/<int:user_id>", methods=["GET"])
def get_user_foods(user_id):
    try:
        validate_user(user_id)
        repo = UserFoodRepository(db)
        user_foods = repo.get_user_foods(user_id)
        return jsonify(user_foods)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route("/confirm_alert", methods=["POST"])
def confirm_alert():
    try:
        data = request.json
        user_id = data["user_id"]
        food_id = data["food_id"]
        shelf_life = data["shelf_life"]

        validate_user(user_id)
        validate_food(food_id)

        repo = UserFoodRepository(db)
        repo.adjust_shelf_life(user_id, food_id, shelf_life)
        expiration_date = datetime.now() + timedelta(days=int(shelf_life))
        repo.add_user_food(user_id, food_id, expiration_date)
        user_foods = repo.get_user_foods(user_id)
        db.session.commit()

        return jsonify(user_foods)

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
