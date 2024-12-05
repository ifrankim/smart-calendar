import os
import requests
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", 1)
USER_ID = int(os.getenv("USER_ID", 1))


class FoodItem:

    @staticmethod
    def get_all():
        try:
            response = requests.get(
                BACKEND_URL + "/get_user_foods/" + str(USER_ID), timeout=400
            )
            print(response.json())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print("Error: The request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"Error: An error occurred with the request: {e}")
        return None

    @staticmethod
    def update_shelf_life(food_id, new_shelf_life):
        try:
            response = requests.post(
                BACKEND_URL + "/confirm_alert",
                json={
                    "user_id": USER_ID,
                    "food_id": food_id,
                    "shelf_life": new_shelf_life,
                },
            )
            print(response.json())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print("Error: The request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"Error: An error occurred with the request: {e}")
        return None