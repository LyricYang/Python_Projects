# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 14:24:38 2018
@author: Administrator

Android手机截屏
"""

import os
from PIL import Image

# 截屏软件调用
def capture_screen(filename="screenshot.png",directory="."):
    os.system("adb shell screencap -p /sdcard/{0}".format(filename))
    os.system("adb pull /sdcard/{0} {1}".format(filename, os.path.join(directory, filename)))

# 对截屏图片进行裁剪
def parse_answer_area(source_file_path, text_area_file):
    image = Image.open(source_file_path)
    wide = image.size[0]
    region = image.crop((100, 330, wide - 70, 550))  #裁剪文字区域
    region.save(text_area_file)

# 读取裁剪后的图片数据
def get_area_data(text_area_file):
    with open(text_area_file, "rb") as fp:
        image_data = fp.read()
        return image_data
    return ""

# 对图片进行处理并返回文字部分的数据
def analyze_current_screen_text(screenshot_filename = "screenshot.png",directory="."):
    save_text_area = os.path.join(directory, "text_area.png")
    capture_screen(screenshot_filename, directory)
    parse_answer_area(os.path.join(directory, screenshot_filename), save_text_area)
    return get_area_data(save_text_area)