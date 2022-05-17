# -*- coding:utf-8 -*-

# Time:2022/05/08 23:12

# OldAuthor:Chiser

# Author:Ryen

import time

import requests

import json

import datetime

from urllib import parse

def get_page(item):

    try:

        if 'action' in item.keys():

            data = {

                'action': 'sign_in'

            }

            response = requests.post(item['url'], headers=headers, data=data)

        elif 'data' in item.keys():

            data = {item['data']}

            response = requests.post(item['url'], headers=headers, data=data)

        else:

            response = requests.get(item['url'], headers=headers)

        time.sleep(3)

        if response.status_code == 200:

            time.sleep(3)

            response = response.text

            if '签到成功' in response or '恭喜您' in response:

                site = ok_site + item['site'] + res_ok

                send_txt.append(site)

            elif '重复刷新' in response or '重复' in response or '簽到過' in response or '已经打卡' or '签到过' in response:

                site = ok_site + item['site'] + res_ok

                send_txt.append(site)

            elif '首页' or '首頁' in response:

                site = ok_site + item['site'] + res_ok

                send_txt.append(site)

        else:

            site = err_site + item['site'] + res_err

            send_txt.append(site)

    except:

        site = err_site + item['site'] + res_err

        send_txt.append(site)

if __name__ == '__main__':

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50'

    json_data = open('site.json', encoding='utf-8')

    json_data = json.load(json_data)

    send_txt = []

    # urlcode编码

    ok_site = '%3Ccenter%3E%3Cb%3E%3Cfont%20color%3D%22%234CAF50%22%3E'

    err_site = '%3Ccenter%3E%3Cb%3E%3Cfont%20color%3D%22%23BF360C%22%3E'

    res_ok = '%5B%E7%AD%BE%E5%88%B0%E6%88%90%E5%8A%9F%7E%5D%3C%2Ffont%3E%3C%2Fb%3E%3C%2Fcenter%3E%3Cbr%3E'

    res_err = '%5B%E7%BD%91%E7%AB%99%E6%97%A0%E6%B3%95%E8%AE%BF%E9%97%AE%7E%5D%3C%2Ffont%3E%3C%2Fb%3E%3C%2Fcenter%3E%3Cbr%3E'

    for item in json_data:

        try:

            if item['referer']:

                headers = {

                    'user-agent': user_agent,

                    'referer': item['referer'],

                    'cookie': item['cookie']

                }

        except:

            headers = {

                'user-agent': user_agent,

                'cookie': item['cookie']

            }

        get_page(item)

    now = datetime.datetime.now()

    time = now.strftime("%Y-%m-%d %H:%M:%S")

    headers = {

        'user_agent': user_agent,

        'Content-type': 'application/x-www-form-urlencoded'

    }

    now_time = '%3Ccenter%3E%3Cb%3E%3Cfont%20color%3D%22%2355a7e3%22%3E' + parse.unquote(time) + '%3C%2Ffont%3E%3C%2Fb%3E%3C%2Fcenter%3E%3Cbr%3E'

    send_txts = ''.join(send_txt)

    # 爱语飞飞推送

    try:

        api = ''

        sen_url = 'https://iyuu.cn/'+api + '.send?text=PT%E7%AD%BE%E5%88%B0%E5%8A%A9%E6%89%8B_v3.0&desp=' + now_time + send_txts

        response = requests.get(sen_url, headers=headers)

        print('爱语飞飞推送成功！')

    except:

        print()

    #pushplus推送

    try:

        token = ''  # 在pushplus网站中可以找到

        title = 'PT签到助手_V3.0新版'  # 改成你要的标题内容

        content = now_time + send_txts  # 改成你要的正文内容

        url = 'http://www.pushplus.plus/send?token=' + token + '&title=' + title + '&content=' + content

        requests.get(url)

        print('pushplus推送成功！')

    except:

        print()

