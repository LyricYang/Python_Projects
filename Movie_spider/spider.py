# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 15:23:52 2017

@author: Administrator
"""

import json
import requests
import re
from requests.exceptions import RequestException
from multiprocessing import Pool

def get_one_page(url):
    #一般用request请求需要异常处理，否则可能导致中断
    try:
        response = requests.get(url)
        if response.status_code == 200:  # 通过状态码来判断是否抓取成功
            return response.text
        return None
    except RequestException:
        return None
'''
    pattern = re.compile('<div class="post">.*?src="(.*?)".*?title"><a'
                         +'.*?>(.*?)</a>.*?rating_nums">(\d+)</span>.*?'
                         +'abstract">(.*?)<br>(.*?)<br>(.*?)<br>(.*?)<br>(.*?)</div>',re.S)
'''  
def parse_one_page(html):
    pattern = re.compile('<div class="post">.*?src="(.*?)".*?</div>.*?'+
                         'title">.*?_blank">(.*?)</a>.*?'+
                         'rating_nums">(.*?)</span>.*?'+
                         'abstract">(.*?)<br />(.*?)<br />(.*?)<br />(.*?)<br />(.*?)</div>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield{'image': item[0],
              'title': item[1].strip(),
              'score': item[2],
              'director': item[3].strip()[3:],
              'actor': item[4].strip()[3:],
              'style': item[5].strip()[3:],
              'country': item[6].strip()[8:],
              'time': item[7].strip()[3:],
                }
def write_to_file(content):
    with open('result.txt','a',encoding = 'utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()
        
def main(offset):
    url='https://www.douban.com/doulist/240962/?start='+str(offset)+'&sort=seq&sub_type='
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    for i in range(4):
        main(i*25)
#    pool = Pool()
#    pool.map(main,[i*25 for i in range(4)])