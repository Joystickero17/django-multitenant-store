import random
from django.contrib.staticfiles import finders
import io
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth import get_user_model

from core.models.store import Store

User = get_user_model()


def image(full_name: str) -> io.BytesIO:
    font_path = finders.find("fonts/Roboto-Bold.ttf")
    print(font_path)
    if full_name:
        try:
            # split the full_name if there are more than one word.
            split = full_name.split(' ')
            # get the fist letter from first two words.
            text = '{}{}'.format(split[0][0], split[1][0])
        except:
            # if the full_name has one word then get the first letter.
            text = full_name[0]

        color_list = [
            (153, 102, 255),
            (000, 102, 255),
            (000, 000, 000),
            (255, 000, 000),
            (255, 153, 000),
            (000, 153, 51),
            (102, 51, 000),
            (204, 000, 153),
        ]
        # get random background colors.
        color = random.choice(color_list)
        image = Image.new('RGB', (288, 288), color=color)
        font_type = ImageFont.truetype(font=font_path,size=150)
        draw = ImageDraw.Draw(image)
        # get height & weight of the text.
        w, h = draw.textsize(text.upper(), font_type)
        draw.text(((288-w)/2, 50), text=text.upper(),
                  fill=(255, 255, 255), font=font_type)
        bynary = io.BytesIO()
        image.save(bynary, "PNG")
        return bynary


def generate_picture_to_django_user(email:str):
    user = User.objects.get(email=email)
    bynary = image(user.full_name)
    user.profile_img.save(f"{user.full_name}.png", bynary)

def generate_picture_to_store(store:Store):
    bynary = image(store.name)
    store.logo.save(f"{store.slug}.png", bynary)