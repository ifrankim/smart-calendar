from controllers.led_controller import LEDController
from models.food_item import FoodItem
from views.calendar_view import render_calendar

led_controller = LEDController()


def update_calendar():
    food_items = FoodItem.get_all()
    led_controller.start_blinking()
    render_calendar(food_items)
    led_controller.stop_blinking()
