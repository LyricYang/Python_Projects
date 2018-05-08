# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-dgktz] <from> <to> <date>

Options:
    -h, --help 查看帮助
    -d         动车
    -g         高铁
    -k         快速
    -t         特快
    -z         直达

Examples:
    tickets 上海 北京 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
#导入模块
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from docopt import docopt
from prettytable import PrettyTable
from colorama import init, Fore
from stations import stations
#防止出现Unverified HTTPS request is being made. Adding certificate verification is strongly advised.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

init()

class TrainsCollection(object):

    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_trains, options):
        self.available_trains = available_trains
        self.options = options

    #处理车次数据，并设置打印格式
	# 'map': {'IFH': '无锡新区', 'NJH': '南京', 'WGH': '无锡东', 'NKH': '南京南', 'WXH': '无锡', 'VCH': '惠山'}
    @property
    def trains(self):
        for raw_train in self.available_trains['result']:
            raw_train=raw_train.split("|")
            train_no = raw_train[3].lower()
            initial = train_no[0]
            if not self.options or initial in self.options:
                from_station_name = self.available_trains['map'].get(raw_train[6])
                to_station_name = self.available_trains['map'].get(raw_train[7])
                start_time = raw_train[8]
                arrive_time = raw_train[9]
                duration = raw_train[10]
                zy_num = raw_train[-4]
                ze_num = raw_train[-5]
                rw_num = raw_train[23]
                yw_num = raw_train[-7]
                yz_num = raw_train[-6]
                wz_num = raw_train[26]
                train = [
                    train_no,        
                    '\n'.join([Fore.GREEN + from_station_name+ Fore.RESET,
                               Fore.RED + to_station_name+ Fore.RESET]),
                    '\n'.join([Fore.GREEN + start_time + Fore.RESET,
                               Fore.RED + arrive_time+ Fore.RESET]),
                    duration,zy_num,ze_num,rw_num,yw_num,yz_num,wz_num
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


def cli():
    """Command-line interface"""
    arguments = docopt(__doc__)
    #从stations.py中获得出发地 目的地
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    """需要修改的地方"""
    #12306网站上请求和响应时的网址
    url = ('https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT').format(date, from_station, to_station)
	#访问请求的格式
    headers={
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Cache-Control':'no-cache',
        'Connection': 'keep-alive',
        'Referer':'https: // kyfw.12306.cn/otn/leftTicket/init',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'X-Requested-With': 'XMLHttpRequest'
        }
    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])
    r = requests.get(url,headers=headers,verify=False)#从网站上请求数据
    print(r.json())
    available_trains = r.json()['data']#将数据信息导出
    TrainsCollection(available_trains, options).pretty_print()#调用打印函数


if __name__ == '__main__':
    cli()
