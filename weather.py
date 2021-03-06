# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# coding:utf-8

import pyttsx3



import os
import re
import time
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }


def numtozh(num):
    num_dict = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七',
                8: '八', 9: '九', 0: '零'}
    num = int(num)
    if 100 <= num < 1000:
        b_num = num // 100
        s_num = (num-b_num*100) // 10
        g_num = (num-b_num*100) % 10
        if g_num == 0 and s_num == 0:
            num = '%s百' % (num_dict[b_num])
        elif s_num == 0:
            num = '%s百%s%s' % (num_dict[b_num], num_dict.get(s_num, ''), num_dict.get(g_num, ''))
        elif g_num == 0:
            num = '%s百%s十' % (num_dict[b_num], num_dict.get(s_num, ''))
        else:
            num = '%s百%s十%s' % (num_dict[b_num], num_dict.get(s_num, ''), num_dict.get(g_num, ''))
    elif 10 <= num < 100:
        s_num = num // 10
        g_num = (num-s_num*10) % 10
        if g_num == 0:
            g_num = ''
        num = '%s十%s' % (num_dict[s_num], num_dict.get(g_num, ''))
    elif 0 <= num < 10:
        g_num = num
        num = '%s' % (num_dict[g_num])
    elif -10 < num < 0:
        g_num = -num
        num = '零下%s' % (num_dict[g_num])
    elif -100 < num <= -10:
        num = -num
        s_num = num // 10
        g_num = (num-s_num*10) % 10
        if g_num == 0:
            g_num = ''
        num = '零下%s十%s' % (num_dict[s_num], num_dict.get(g_num, ''))
    return num

def AMorPM(num):
    try:
        num = int(num)
    except:
        print ('整数转换出错')
    hour_word = "转换出错了"
    if 6 <=num<11  : 
        hour_word = "早上好"
    elif 11 <=num<13  : 
        hour_word = "中午好"
    elif 3 <=num<18  : 
        hour_word = "下午好"
    elif 18<=num<24  : 
        hour_word = "晚上好"
    elif 24<=num<6  : 
        hour_word = "凌晨好"
    else:
        hour_word = '出错了'
    
    return hour_word
    


def get_weather():
    # 下载墨迹天气主页源码
    res = requests.get('http://tianqi.moji.com/', headers=headers)
    # 用BeautifulSoup获取所需信息
    soup = BeautifulSoup(res.text, "html.parser")
    temp = soup.find('div', attrs={'class': 'wea_weather clearfix'}).em.getText()
    temp = numtozh(int(temp))
    weather = soup.find('div', attrs={'class': 'wea_weather clearfix'}).b.getText()
    sd = soup.find('div', attrs={'class': 'wea_about clearfix'}).span.getText()
    sd_num = re.search(r'\d+', sd).group()
    sd_num_zh = numtozh(int(sd_num))
    sd = sd.replace(sd_num, sd_num_zh)
    wind = soup.find('div', attrs={'class': 'wea_about clearfix'}).em.getText()
    aqi = soup.find('div', attrs={'class': 'wea_alert clearfix'}).em.getText()
    aqi_num = re.search(r'\d+', aqi).group()
    aqi_num_zh = numtozh(int(aqi_num))
    aqi = aqi.replace(aqi_num, aqi_num_zh).replace(' ', ',空气质量')
    info = soup.find('div', attrs={'class': 'wea_tips clearfix'}).em.getText()
    sd = sd.replace(' ', '百分之').replace('%', '')
    aqi = '空气质量指数' + aqi
    info = info.replace('，', ',')
    # 获取今天的日期
    today = datetime.now().date().strftime('%Y年%m月%d日')
    #获取时间称呼
    am_pm = AMorPM(time.strftime('%H',time.localtime(time.time())))
    
    
    # 将获取的信息拼接成一句话
    text = '%s,今天是%s,天气%s,温度%s摄氏度,%s,%s,%s,%s' % \
           (am_pm,today, weather, temp, sd, wind, aqi, info)
    return text




def main():
    # 获取需要转换语音的文字
    text = get_weather()
    print(text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    print(time.strftime('%H',time.localtime(time.time())))


if __name__ == '__main__':
    main()