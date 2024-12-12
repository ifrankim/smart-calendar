from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont


def render_alert(food_name, expiration_date, shelf_life):
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    screen_width, screen_height = epd.width, epd.height
    alert_width, alert_height = 300, 200

    Xstart = (screen_width - alert_width) // 2
    Ystart = (screen_height - alert_height) // 2

    alert_image = Image.new("1", (screen_width, screen_height), 255)
    draw = ImageDraw.Draw(alert_image)

    font_title = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24
    )
    font_body = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20
    )
    font_body_btn = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60
    )

    draw.rectangle(
        (Xstart, Ystart, Xstart + alert_width, Ystart + alert_height),
        outline=0,
        fill=255,
    )

    draw.text(
        (Xstart + 50, Ystart + 50),
        f"Food: {food_name}".title(),
        font=font_title,
        fill=0,
    )
    draw.text(
        (Xstart + 50, Ystart + 90),
        f"Expires: {expiration_date.strftime('%Y-%m-%d')}",
        font=font_body,
        fill=0,
    )
    draw.text(
        (Xstart + 50, Ystart + 130),
        f"Shelf Life: {shelf_life} days",
        font=font_body,
        fill=0,
    )

    button_x = screen_width - 100
    draw.text((button_x + 15, Ystart - 55), "+", font=font_body_btn, fill=0)
    draw.text((button_x, Ystart + 100), "Confirm", font=font_body, fill=0)
    draw.text((button_x + 25, Ystart + 210), "-", font=font_body_btn, fill=0)

    alert_image.save("alert5.jpg")
    epd.display(epd.getbuffer(alert_image))
