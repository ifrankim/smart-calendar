import requests
from eink_display import render_calendar
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:5000"


def fetch_calendar_data(user_id):
    today = datetime.now()
    day_of_month = today.day
    try:
        response = requests.get(f"{BACKEND_URL}/get_user_foods/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar dados: {e}")
        return []


if __name__ == "__main__":
    user_id = 0
    calendar_data = fetch_calendar_data(user_id)
    render_calendar(calendar_data)
