#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 11:45 AM
# @Author  : NeiL Liu
# @File    : main.py
# @Project ：xunacg_autosign
# @Software: PyCharm

import re
import sys
import time
import urllib3
import hashlib
import datetime
import requests
from bs4 import BeautifulSoup
from config import config

urllib3.disable_warnings()  # 停止SSL報錯
session = requests.Session()  # 取得Session，以便後續簽到使用
session.keep_alive = False  # 關閉多餘連線

# config
accounts = config.get('accounts')
url = config.get('url')
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
coins = 0


# str轉md5
def str2md5(pass_str):
    return hashlib.md5(pass_str.encode('utf-8')).hexdigest()


# 字串取數字
def findint(result):
    intlist = [int(s) for s in re.findall(r'-?\d+\.?\d*', result)]
    return intlist


# 登入
def login(email, password, uid):
    global coins
    data = {
        'email': email,
        'password': str2md5(password),
    }
    try:
        login_res = session.post(url['login_url'], headers=headers, data=data, verify=False)
        if login_res.status_code == 200:
            soup = BeautifulSoup(login_res.text, "html5lib")
            result = soup.find('h4').text.strip('\n')
            print(result)
            coins = 0
            dailysign_msg = dailysign()
            freecoin(uid)
            push_msg(dailysign_msg)
    except requests.exceptions.RequestException as e:
        print(f'Login錯誤訊息：{e}')


# 每日簽到
def dailysign():
    global coins
    try:
        dailysign_res = session.post(url['dailysign_url'], headers=headers, verify=False)
        if dailysign_res.status_code == 200:
            soup = BeautifulSoup(dailysign_res.text, "html5lib")
            result = soup.find('h4').text.strip('\n')
            dailysign_msg = f'每日簽到狀態：{result}'
            getint = findint(result)
            coins += getint[1]
            return dailysign_msg
        dailysign_res.close()
    except requests.exceptions.RequestException as e:
        print(f'錯誤訊息：{e}')


# 取得當日coin免費次數
def getcoincount():
    try:
        getcoincount_res = session.get(url['freecoin_url'], headers=headers, verify=False)
        soup = BeautifulSoup(getcoincount_res.text, "html5lib")
        result = soup.find("h4").text.strip('\n')
        getint = findint(result)  # 將字串中數字提取出來
        totalruns = getint[2] if len(getint) != 4 else getint[3]
        # print(f'白嫖下載卷需跑{totalruns}次，間隔35秒。')
        getcoincount_res.close()
        return totalruns
    except requests.exceptions.RequestException as e:
        print(f'錯誤訊息：{e}')


# freecoin簽到
def freecoin(uid):
    totalruns = getcoincount()  # 取得當日coin免費次數
    global coins
    data = {
        'uid': uid
    }
    for i in range(1, totalruns + 1):
        for j in range(1, 36):
            print("\r", end="")
            print("等待時間(35s): {}s: ".format(j), "▓" * j, end="")
            sys.stdout.flush()
            time.sleep(1)
        try:
            freecoin_res = session.post(url['freecoin_url'], headers=headers, data=data, verify=False)
            if freecoin_res.status_code == 200:
                soup = BeautifulSoup(freecoin_res.text, "html5lib")
                result = soup.find('h4').text.strip('\n')
                getint = findint(result)
                coins += getint[0]
                print(f'\n{datetime.datetime.now()} {result} 已完成{i}次，還需{totalruns - i}次。')
        except requests.exceptions.RequestException as e:
            print(f'錯誤訊息：{e}')
    # print(f'coins總共有：{coins}個。')


def push_msg(dailysign_msg):
    pushmsg = f'''{datetime.datetime.now()}
    {dailysign_msg}
    今日總共取得：{coins}個。
    '''
    print(pushmsg)


if __name__ == '__main__':

    for account in accounts:
        login(account['email'], account['password'], account['uid'])
