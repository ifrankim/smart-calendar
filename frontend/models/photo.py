from picamera2 import Picamera2
import os
import requests
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", 1)
USER_ID = int(os.getenv("USER_ID", 1))


class Photo:
    @staticmethod
    def capture():
        picam2 = None
        try:
            picam2 = Picamera2()
            picam2.configure(picam2.create_still_configuration())
            file_name = "food_photo.jpg"
            picam2.start()
            picam2.capture_file(file_name)
            picam2.stop()
            return file_name
        finally:
            if picam2 is not None:
                picam2.close()

    @staticmethod
    def send_to_backend(file_path):
        print(file_path)
        try:
            print(f"Sending file: {file_path} for user_id: {USER_ID}")
            with open(file_path, "rb") as img:
                response = requests.post(
                    BACKEND_URL + "/scan_food",
                    data={"user_id": USER_ID},
                    files={"image": img},
                )

            print(BACKEND_URL + "/scan_food")
            response.raise_for_status()
            print(response.json())
            return response.json()
        except requests.exceptions.Timeout:
            print("Error: The request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"Error: An error occurred with the request: {e}")
        return {"food": "", "shelf_life": ""}
