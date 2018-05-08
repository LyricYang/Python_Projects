# -*- coding: utf-8 -*-
import time
import datetime
import sys
from imp import reload
reload(sys)

DB = [
0x04bd8,0x04ae0,0x0a570,0x054d5,0x0d260,0x0d950,0x16554,0x056a0,0x09ad0,0x055d2,
0x04ae0,0x0a5b6,0x0a4d0,0x0d250,0x1d255,0x0b540,0x0d6a0,0x0ada2,0x095b0,0x14977,
0x04970,0x0a4b0,0x0b4b5,0x06a50,0x06d40,0x1ab54,0x02b60,0x09570,0x052f2,0x04970,
0x06566,0x0d4a0,0x0ea50,0x06e95,0x05ad0,0x02b60,0x186e3,0x092e0,0x1c8d7,0x0c950,
0x0d4a0,0x1d8a6,0x0b550,0x056a0,0x1a5b4,0x025d0,0x092d0,0x0d2b2,0x0a950,0x0b557,
0x06ca0,0x0b550,0x15355,0x04da0,0x0a5b0,0x14573,0x052b0,0x0a9a8,0x0e950,0x06aa0,
0x0aea6,0x0ab50,0x04b60,0x0aae4,0x0a570,0x05260,0x0f263,0x0d950,0x05b57,0x056a0,
0x096d0,0x04dd5,0x04ad0,0x0a4d0,0x0d4d4,0x0d250,0x0d558,0x0b540,0x0b6a0,0x195a6,
0x095b0,0x049b0,0x0a974,0x0a4b0,0x0b27a,0x06a50,0x06d40,0x0af46,0x0ab60,0x09570,
0x04af5,0x04970,0x064b0,0x074a3,0x0ea50,0x06b58,0x055c0,0x0ab60,0x096d5,0x092e0,
0x0c960,0x0d954,0x0d4a0,0x0da50,0x07552,0x056a0,0x0abb7,0x025d0,0x092d0,0x0cab5,
0x0a950,0x0b4a0,0x0baa4,0x0ad50,0x055d9,0x04ba0,0x0a5b0,0x15176,0x052b0,0x0a930,
0x07954,0x06aa0,0x0ad50,0x05b52,0x04b60,0x0a6e6,0x0a4e0,0x0d260,0x0ea65,0x0d530,
0x05aa0,0x076a3,0x096d0,0x04bd7,0x04ad0,0x0a4d0,0x1d0b6,0x0d250,0x0d520,0x0dd45,
0x0b5a0,0x056d0,0x055b2,0x049b0,0x0a577,0x0a4b0,0x0aa50,0x1b255,0x06d20,0x0ada0,
0x14b63]
"""
前4位表示闰大月或闰小月，0为闰小月29天，1为闰大月30天
中间12位表示12个月的大小，0为小月29填，1为大月30天
后4位表示闰月是几月，0表示此年没有闰月
农历1900正月初一是公历的1900年1月31日
"""
#--------------
#农历相关计算函数
#--------------
	#闰月是哪月
def Rmonth_year(y):
	return 0x0000f & DB[y]

	#闰月有多少天
def Rmonth_days_year(y):
	if Rmonth_year(y) == 0:
		return 0
	elif 0x10000 & DB[y] == 0x10000:
		return 30
	else:
		return 29

	#某年某月的天数
def days_month(y,m):
	i = (0x08000 >> m)
	if i & DB[y] == i:
		return 30
	else:
		return 29

	#返回某年的月列表
def days_year_months(y):
	i = 0
	list_months = []
	while i < 12:
		list_months.append(days_month(y,i))
		if i == (Rmonth_year(y) - 1):
			list_months.append(Rmonth_days_year(y))
		i = i + 1
	return list_months

	#某年的总天数
def days_year(year):
	list_months = days_year_months(year)
	days = 0
	for month_days in list_months:
		days = days + month_days
	return days

	#通过天数推算农历月
def get_month(year,days):
	i = 0
	month = 0
	while i < days:
		i = i + days_year_months(year)[month]
		month = month + 1
	return month

	#通过天数计算农历的年月日
def get_year_month_day(days):
	#计算年份
	year_days = 0
	year = 0
	while year_days <= days:
		year_days = year_days + days_year(year)
		year = year + 1
	year = year - 1
	year_days = year_days - days_year(year)
	
	#计算月份
	days = days - year_days
	month_days = 0
	month = 0
	while month_days <= days:
		month_days = month_days + days_year_months(year)[month]
		month = month + 1
	month = month - 1
	month_days = month_days - days_year_months(year)[month]
	
	#计算天数
	days = days - month_days

	#显示月份（之前计算的月份表示的是该月是此年的第几个月可能会出现第13个月，并不考虑闰月的显示）
	if Rmonth_days_year(year) == 0:
		month_s = '%d' % (month + 1)
	elif month <= Rmonth_year(year) - 1:
		month_s = '%d'% (month + 1)
	elif month == Rmonth_year(year):
		month_s = 'R%d' % month#R代表闰月
	else:
		month_s = '%d'% month

	return (year+1900,month_s,days+1)

#测试模块
i = datetime.datetime(2018,5,8)
days2zero = (i - datetime.datetime(1900,1,31)).days
print('G',i)
print('L',get_year_month_day(days2zero))

