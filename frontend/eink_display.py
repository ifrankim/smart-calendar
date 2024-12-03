import calendar
from datetime import datetime, timedelta
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont

from gpiozero import Button
import requests


def display_calendar(calendar_data):
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    image = Image.new("1", (epd.height, epd.width), 255)
    image = image.transpose(Image.ROTATE_90)
    draw = ImageDraw.Draw(image)

    font_title = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28
    )
    font_week = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24
    )
    font_days = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16
    )

    today = datetime.now()
    month_number = today.month
    month_name = calendar.month_name[month_number]
    title = f"{month_name} {today.year}"
    draw.text((250, 10), title, font=font_title, fill=0)

    days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    x_start = 10
    y_start = 60
    cell_width = 111
    cell_height = 70

    for i, day in enumerate(days_of_week):
        draw.text((x_start + i * cell_width + 20, y_start), day, font=font_week, fill=0)

    y_start += 40
    for week in range(5):
        for day in range(7):
            x0 = x_start + day * cell_width
            y0 = y_start + week * cell_height
            x1 = x0 + cell_width
            y1 = y0 + cell_height
            draw.rectangle([x0, y0, x1, y1], outline=0)

    cal = calendar.Calendar(firstweekday=6)
    days = cal.itermonthdays(today.year, today.month)

    expiration_dict = {}
    for item in calendar_data:
        date = datetime.strptime(item["expiration_date"], "%Y-%m-%d")
        if date.month == today.month and date.year == today.year:
            expiration_dict[date.day] = item["food"]

    x_offset = x_start
    y_offset = y_start
    for day in days:
        if day != 0:
            draw.text((x_offset + 10, y_offset + 5), str(day), font=font_days, fill=0)
            if day in expiration_dict:
                draw.text(
                    (x_offset + 10, y_offset + 25),
                    expiration_dict[day],
                    font=font_days,
                    fill=0,
                )

        x_offset += cell_width
        if x_offset >= x_start + 7 * cell_width:
            x_offset = x_start
            y_offset += cell_height

    epd.display(epd.getbuffer(image))
    epd.sleep()


calendar_data = [
    {"food": "Banana", "expiration_date": "2024-12-05"},
    {"food": "Milk", "expiration_date": "2024-12-27"},
]


# Configurações de hardware
button_minus = Button(13)  # GPIO pin para o botão de -
button_plus = Button(27)  # GPIO pin para o botão de +
button_confirm = Button(22)  # GPIO pin para o botão de confirmar

# Configuração do backend
BACKEND_URL = "http://127.0.0.1:5000"


def take_photo_and_call_backend():
    # Simulação de chamada ao backend
    # Envie a imagem aqui e processe o retorno
    response = requests.post(
        f"{BACKEND_URL}/process_image", files={"image": open("photo.jpg", "rb")}
    )
    response_data = response.json()
    return response_data


def display_alert(food_name, initial_shelf_life):
    # Inicializa a tela
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    # Configurações da imagem
    image = Image.new("1", (epd.height, epd.width), 255)
    image = image.transpose(Image.ROTATE_90)
    draw = ImageDraw.Draw(image)

    # Fonte
    font_title = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28
    )
    font_buttons = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24
    )

    # Configuração inicial
    shelf_life = initial_shelf_life
    expiration_date = datetime.now() + timedelta(days=shelf_life)

    # Funções para os botões
    def update_display():
        draw.rectangle((0, 0, epd.width, epd.height), fill=255)  # Limpa a tela
        draw.text((50, 20), f"Food: {food_name}", font=font_title, fill=0)
        draw.text(
            (50, 70),
            f"Expires: {expiration_date.strftime('%Y-%m-%d')}",
            font=font_title,
            fill=0,
        )
        draw.text((50, 150), "-  Confirm  +", font=font_buttons, fill=0)
        epd.display(epd.getbuffer(image))

    def decrease_days():
        nonlocal shelf_life, expiration_date
        shelf_life -= 1
        expiration_date = datetime.now() + timedelta(days=shelf_life)
        update_display()

    def increase_days():
        nonlocal shelf_life, expiration_date
        shelf_life += 1
        expiration_date = datetime.now() + timedelta(days=shelf_life)
        update_display()

    def confirm():
        print(f"Confirmed: {food_name}, {expiration_date.strftime('%Y-%m-%d')}")
        epd.Clear()
        epd.sleep()

    # Liga os botões às funções
    button_minus.when_pressed = decrease_days
    button_plus.when_pressed = increase_days
    button_confirm.when_pressed = confirm

    update_display()


if __name__ == "__main__":
    display_calendar(calendar_data)

    backend_response = {"food": "banana", "shelf_life": 7}

    # display_alert(backend_response["food"], backend_response["shelf_life"])
