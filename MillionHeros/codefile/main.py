# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 14:41:55 2018
@author: Administrator

主函数
"""

from config import app_id
from config import app_key
from config import app_secret
from config import data_directory
from config import hanwan_appcode
from config import search_url
from config import prefer
from config import timevisual
import time           #时间检测模块
import json
import base64
import requests
import process
import urllib.request
import re
from aip import AipOcr
from androidscreenshot import analyze_current_screen_text



def Optical_Character_Recognition(pre,image_data):
    if pre[0]=="baidu":
        timeout=3
        text_from_image = get_text_baidu(image_data,app_id,app_key,app_secret,timeout)
    elif pre[0]=="hanwang":
        timeout=3
        text_from_image = get_text_hanwang(image_data, hanwan_appcode, timeout)
    else:
        print("OCR Selection Error!")
    return text_from_image

# 百度文字识别
def get_text_baidu(image_data, app_id, app_key, app_secret, timeout=3):
    client = AipOcr(appId=app_id, apiKey=app_key, secretKey=app_secret)
    client.setConnectionTimeoutInMillis(timeout*1000)
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"
    result = client.basicGeneral(image_data, options)
    if "error_code" in result:
        print("baidu api error: ", result["error_msg"])
        return ""
    return "".join([words["words"] for words in result["words_result"]])

# 汉王文字识别
def get_text_hanwang(image_data, appcode, timeout=3):
    s=bytes.decode(base64.b64encode(image_data)) 
    data = "{\"uid\":\"118.12.0.12\",\"lang\":\"chns\",\"color\":\"color\",\"image\":\"" +s+ "\"}"
    base_url = "http://text.aliapi.hanvon.com/rt/ws/v1/ocr/text/recg"
    request = urllib.request.Request(base_url, str.encode(data))
    request.add_header('Authorization', 'APPCODE ' + appcode)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    request.add_header('Content-Type', 'application/octet-stream')
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        decode_json = json.loads(content)
    return ''.join(decode_json['textResult'].split())
# 
def page(word):
    r = requests.get(search_url + word)
    if r.status_code == 200:
        return r.text
    else:
        print(r.status_code)
        return False
# 百度搜索
def search(keyword, **kwargs):
    kwargs.setdefault('convey', False)
    search_page = page(keyword)
    results = process.page(search_page)
    if kwargs['convey']:
        for result in results:
            result.convey_url()
    return results    
    
def main():
    # 文字识别
    start = time.time()
    screenshot_filename = "screenshot.png"
    image_data = analyze_current_screen_text(screenshot_filename,data_directory)
    question_text = Optical_Character_Recognition(prefer,image_data)
    keyword = question_text[2:]
    print("问题："+keyword+"\n")
    filtrate = re.compile(u'[^\u4E00-\u9FA5]')#非中文
    keyword = filtrate.sub(r'', keyword)
    # 搜索问题
    convey = 'n'
    if convey == 'y' or convey == 'Y':
        results = search(keyword, convey=True)
    elif convey == 'n' or convey == 'N' or not convey:
        results = search(keyword)
    else:
        print('输入错误')
        exit(0)
    # 搜索结果处理
    count = 0
    for result in results:
        if(result.abstract.find("更多关于")):
            index=result.abstract.find("更多关于")
            temp=result.abstract[:index]
        else:
            temp=result.abstract
        print('{0}{1}'.format("  ",temp)),print('\n')  # 此处应有格式化输出
        count=count+1
        if(count == 3):
            break
    # 时间显示
    if timevisual:
        end=time.time()
        print("TIME INTERVAL : "+str(end-start)+'s')
    
if __name__=="__main__":
    import cProfile
    cProfile.run("main()",filename="result.txt")