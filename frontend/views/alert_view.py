from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont


def render_alert(food_name, expiration_date, shelf_life):
    """
    Renderiza o alerta no meio da tela usando `display_Partial`.
    """
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

    draw.rectangle((Xstart, Ystart, alert_width, alert_height), outline=0, fill=255)
    draw.text((Xstart + 10, Ystart + 10), f"Food: {food_name}", font=font_title, fill=0)
    draw.text(
        (Xstart + 10, Ystart + 50),
        f"Expires: {expiration_date.strftime('%Y-%m-%d')}",
        font=font_body,
        fill=0,
    )
    draw.text(
        (Xstart + 10, Ystart + 90),
        f"Shelf Life: {shelf_life} days",
        font=font_body,
        fill=0,
    )
    draw.text((Xstart + 10, Ystart + 150), "-  Confirm  +", font=font_body, fill=0)

    epd.display(epd.getbuffer(alert_image))
