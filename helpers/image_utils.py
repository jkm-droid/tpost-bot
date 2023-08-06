import os
from datetime import datetime

from PIL import ImageDraw, ImageFont, Image


def wrap_text(image, text, font_type, font_size):
    width = 750
    height = 500
    image = Image.open(image).resize((width, height))
    draw = ImageDraw.Draw(image, "RGBA")

    quote = text
    text_width = width * 0.8
    text_max_height = height * 0.8

    while font_size > 9:
        font = ImageFont.truetype(font_type, font_size, layout_engine=ImageFont.Layout.BASIC)
        lines = []
        line = ""
        for word in quote.split():
            proposed_line = line
            if line:
                proposed_line += " "
            proposed_line += word
            if font.getlength(proposed_line) <= text_width:
                line = proposed_line
            else:
                # If this word was added, the line would be too long
                # Start a new line instead
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        quote = "\n".join(lines)

        x1, y1, x2, y2 = draw.multiline_textbbox((0, 0), quote, font, stroke_width=1)
        w, h = x2 - x1, y2 - y1
        if h <= text_max_height:
            break
        else:
            # The text did not fit comfortably into the image
            # Try again at a smaller font size
            font_size -= 1

    draw.multiline_text((width / 2 - w / 2 - x1, height / 2 - h / 2 - y1),
                        quote,
                        font=font,
                        align="center",
                        stroke_width=2,
                        stroke_fill="#000")

    current_data_time = datetime.now()
    date = current_data_time.strftime("%Y-%m-%d-%H:%M")
    image.save(f"{os.getcwd()}/assets/quotes/quote-{date}")
    image.show()
