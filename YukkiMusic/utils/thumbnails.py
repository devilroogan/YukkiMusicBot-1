#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import os
import re
import textwrap

import aiofiles
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch

from config import MUSIC_BOT_NAME, YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    if image.size[0] == image.size[1]:
        # Does not change the scale of the orientation image and displays it centered.
        # It may look even better
        newImage = image.resize((maxHeight, maxHeight))
        img = Image.new("RGBA", (maxWidth, maxHeight))
        img.paste(newImage, (int((maxWidth - maxHeight) / 2), 0))
        return img
    else:
        widthRatio = maxWidth / image.size[0]
        heightRatio = maxHeight / image.size[1]
        newWidth = int(widthRatio * image.size[0])
        newHeight = int(heightRatio * image.size[1])
        newImage = image.resize((newWidth, newHeight))
    return newImage


async def thumb(thumbnail, title, userid, ctitle):
    img_path = f"search/thumb{userid}.png"
    if 'http' in thumbnail:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(img_path, mode="wb")
                    await f.write(await resp.read())
                    await f.close()
    else:
        img_path = thumbnail
    image1 = Image.open(img_path)
    image2 = Image.open("assets/LightGreen.png")
    image3 = changeImageSize(1280, 720, image1) 
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save(f"search/temp{userid}.png")
    img = Image.open(f"search/temp{userid}.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("assets/regular.ttf", 50)
    font2 = ImageFont.truetype("assets/medium.ttf", 72)
    
    img.save(f"search/final{userid}.png")
    os.remove(f"search/temp{userid}.png")
    os.remove(img_path)
    final = f"search/final{userid}.png"
    return final
