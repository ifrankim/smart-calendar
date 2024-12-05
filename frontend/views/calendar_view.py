import calendar
from datetime import datetime, timedelta
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont


def render_calendar(calendar_data):
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
            if date.day not in expiration_dict:
                expiration_dict[date.day] = []
            expiration_dict[date.day].append(item["food_name"].title())

    x_offset = x_start
    y_offset = y_start
    for day in days:
        if day != 0:
            draw.text((x_offset + 10, y_offset + 5), str(day), font=font_days, fill=0)
            if day in expiration_dict:
                foods = expiration_dict[day]
                num_foods = len(foods)

                max_font_size = 14
                adjusted_font_size = max_font_size
                if num_foods > 2:
                    adjusted_font_size = max(8, max_font_size - (num_foods - 2) * 2)
                dynamic_font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    adjusted_font_size,
                )

                line_height = cell_height * 0.9 // (num_foods + 1)
                for i, food in enumerate(foods):
                    draw.text(
                        (x_offset + 10, y_offset + 23 + i * line_height),
                        food,
                        font=dynamic_font,
                        fill=0,
                    )

        x_offset += cell_width
        if x_offset >= x_start + 7 * cell_width:
            x_offset = x_start
            y_offset += cell_height

    epd.display(epd.getbuffer(image))
    epd.sleep()
