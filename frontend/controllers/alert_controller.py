from gpiozero import Button
from datetime import datetime, timedelta
from views.alert_view import render_alert
from models.food_item import FoodItem
from controllers.calendar_controller import update_calendar
from controllers.led_controller import LEDController

button_minus = Button(16, bounce_time=1.0)
button_plus = Button(19, bounce_time=1.0)
button_confirm = Button(26, bounce_time=1.0)
led_controller = LEDController()


def handle_alert(food_name, food_id, initial_shelf_life):
    shelf_life = initial_shelf_life
    expiration_date = datetime.now() + timedelta(days=shelf_life)

    def decrease_days():
        led_controller.start_blinking()
        nonlocal shelf_life, expiration_date
        shelf_life -= 1
        expiration_date = datetime.now() + timedelta(days=shelf_life)
        render_alert(food_name, expiration_date, shelf_life)
        led_controller.stop_blinking()

    def increase_days():
        led_controller.start_blinking()
        nonlocal shelf_life, expiration_date
        shelf_life += 1
        expiration_date = datetime.now() + timedelta(days=shelf_life)
        render_alert(food_name, expiration_date, shelf_life)
        led_controller.stop_blinking()

    def confirm():
        print(f"Confirmed: {food_name}, Shelf Life: {shelf_life} days")
        FoodItem.update_shelf_life(food_id, shelf_life)
        update_calendar()

    button_minus.when_pressed = decrease_days
    button_plus.when_pressed = increase_days
    button_confirm.when_pressed = confirm

    render_alert(food_name, expiration_date, shelf_life)
