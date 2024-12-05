from models.food_item import FoodItem
from views.calendar_view import render_calendar


def update_calendar():
    food_items = FoodItem.get_all()
    render_calendar(food_items)
