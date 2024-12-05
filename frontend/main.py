import time
from gpiozero import Button
from controllers.calendar_controller import update_calendar
from controllers.camera_controller import capture_and_process
from controllers.alert_controller import handle_alert

button_photo = Button(5, bounce_time=1.0)


def capture_photo_interrupt():
    button_photo.wait_for_press()
    print("Button pressed! Capturing photo...")
    result = capture_and_process()
    # result = {'category': None, 'food': 'pineapple', 'food_item_id': 4, 'shelf_life': 5}
    if result["food"] == "":
        pass
    else:
        handle_alert(result["food"], result["food_item_id"], int(result["shelf_life"]))


def main():
    button_photo.when_pressed = capture_photo_interrupt

    while True:
        print("Updating calendar...")
        update_calendar()
        print("Calendar updated. Sleeping for 12 hours...")
        time.sleep(12 * 60 * 60)


if __name__ == "__main__":
    main()
