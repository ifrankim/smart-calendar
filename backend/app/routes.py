from flask import Blueprint, request, jsonify
from app.models import User, FoodItem, UserFood
from app import db
from datetime import datetime, timedelta
from app.services import process_image


routes = Blueprint("routes", __name__)


@routes.route("/process_image", methods=["POST"])
def process_image_route():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded."}), 400
    image = request.files["image"]
    detected_items = process_image(image)
    return jsonify(detected_items)


# Rota para criar um novo usuário
@routes.route("/create_user", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(name=data["name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuário criado com sucesso!", "user_id": new_user.id})


# Rota para adicionar um novo item global de comida
@routes.route("/add_food_item", methods=["POST"])
def add_food_item():
    data = request.json
    food_item = FoodItem(
        name=data["name"],
        category=data.get("category", "Uncategorized"),
        shelf_life=data.get("shelf_life", 7),
        adjustments=data.get("adjustments", []),
    )
    db.session.add(food_item)
    db.session.commit()
    return jsonify(
        {
            "message": "Item de comida adicionado com sucesso!",
            "food_item_id": food_item.id,
        }
    )


# Rota para associar um item de comida a um usuário
@routes.route("/add_user_food", methods=["POST"])
def add_user_food():
    data = request.json
    user_id = data["user_id"]
    food_item_id = data["food_item_id"]

    # Calcular data de validade
    food_item = FoodItem.query.get(food_item_id)
    expiration_date = datetime.now() + timedelta(days=food_item.shelf_life)

    # Criar associação
    user_food = UserFood(
        user_id=user_id,
        food_item_id=food_item_id,
        expiration_date=expiration_date,
        adjustments=[],
    )
    db.session.add(user_food)
    db.session.commit()

    return jsonify(
        {
            "message": f"{food_item.name} foi adicionado ao usuário {user_id}!",
            "expiration_date": expiration_date.date().isoformat(),
        }
    )


# Rota para listar todos os itens de comida globalmente
@routes.route("/get_food_items", methods=["GET"])
def get_food_items():
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


# Rota para obter um item de comida pelo ID
@routes.route("/get_food_item_by_id/<int:food_item_id>", methods=["GET"])
def get_food_item_by_id(food_item_id):
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


# Rota para obter um item de comida pelo nome
@routes.route("/get_food_item_by_name", methods=["GET"])
def get_food_item_by_name():
    name = request.args.get("name")  # Query parameter
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


# Rota para listar as comidas associadas a um usuário
@routes.route("/get_user_foods/<int:user_id>", methods=["GET"])
def get_user_foods(user_id):
    user_foods = UserFood.query.filter_by(user_id=user_id).all()
    result = [
        {
            "food_name": uf.food_item.name,
            "expiration_date": uf.expiration_date.date().isoformat(),
            "adjustments": uf.adjustments,
        }
        for uf in user_foods
    ]
    return jsonify(result)


# Rota para ajustar a validade de uma comida do usuário
@routes.route("/adjust_user_food", methods=["POST"])
def adjust_user_food():
    data = request.json
    user_food = UserFood.query.get(data["user_food_id"])

    # Registrar ajuste
    adjustment = {"user_id": data["user_id"], "adjustment": data["adjustment"]}
    user_food.adjustments.append(adjustment)

    # Ajustar data de validade
    user_food.expiration_date += timedelta(days=data["adjustment"])

    db.session.commit()
    return jsonify(
        {
            "message": "Ajuste realizado com sucesso!",
            "new_expiration_date": user_food.expiration_date.date().isoformat(),
        }
    )
