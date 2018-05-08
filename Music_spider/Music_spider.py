# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 14:40:54 2017

@author: Administrator
"""

# -*- coding:utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
import requests
import json
import re
import os

def get_music_ids_by_singer_id(singer_ID):
    url = r'http://music.163.com/artist?id=' + str(singer_ID)
    req = request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
    resp = request.urlopen(req).read().decode('utf-8')
    soup = bs(resp,'html.parser')
    singer_name = soup.select("#artist-name")[0].get('title')
    t = soup.find('textarea')
    musics = json.loads(t.text.replace('(','[').replace(')',']'))
    ids ={}
    for music in musics:
        ids[music['name']] = music['id']
    return ids,singer_name

def get_lyric_by_music_ids(music_id):
    lrc_url = r'http://music.163.com/api/song/lyric?' + 'id=' + str(music_id) + '&lv=1&kv=1&tv=-1'
    resp = requests.get(lrc_url).text
    j = json.loads(resp)
    try:#部分歌曲没有歌词，这里引入一个异常
        lrc = j['lrc']['lyric']
        pat = re.compile(r'\[.*\]')#下面这三行正则匹配删除时间轴
        lrc = re.sub(pat,"",lrc)
        lrc = lrc.rstrip()
        return lrc
    except KeyError as e:
        pass

def mkdir(path):
    path = path.strip() # 去除首位空格
    path = path.rstrip("\\")# 去除尾部 \ 符号
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def func(singer_ID):
    music_ids,singer_name = get_music_ids_by_singer_id(singer_ID)
    singer_name = singer_name.split(' -')[0]
    dirpath = 'C:\\Users\\Administrator\\Desktop\\Python\\PROJECT\\Music_spider\\'+singer_name
    filepath = dirpath + '\\'
    mkdir(dirpath)
    for key in music_ids:
        lyric_content = get_lyric_by_music_ids(music_ids[key])
        f = open(filepath + key +'.txt', 'w',encoding='utf-8')
        try:  # 引入异常
            f.write(lyric_content)
            f.close()
        except AttributeError as e2:
            pass
     
        
if __name__=='__main__':
    singer_ID = [2116,3684,96266]
    for i in range(3):
        func(singer_ID[i])
        
    