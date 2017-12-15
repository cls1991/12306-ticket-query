# coding: utf8

"""
工具集
"""

import datetime
import json
import re
import sys
import time

import requests
from prettytable import PrettyTable

from share import const


def request_html(url, method='GET', headers=None, proxies=None):
    """
    send request
    :param url:
    :param method:
    :param headers:
    :param proxies:
    :return:
    """
    resp = None
    try:
        r = requests.request(method, url, headers=headers, proxies=proxies)
        if r.status_code == 200:
            resp = r.text
    except requests.RequestException as e:
        print(e)

    return resp


def generate_station_name_pairs(use_local_file=True):
    """
    generate snp
    :param use_local_file:
    :return:
    """
    if use_local_file:
        with open('data/station_name.js', 'rb') as f:
            sd = f.read().decode('utf8').replace('\n', '')
        rs = dict()
        res = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', sd)
        for r in res:
            rs[r[0]] = r[1]
        if rs:
            with open('data/station_name.json', 'wb') as f:
                f.write(json.dumps(rs, indent=4).encode())


def copy_dict_by_keys(s, t, keys):
    """
    copy dict k/v pairs from s to t
    """
    for key in keys:
        if key in s:
            t.append(s[key])


def pretty_print(header, data):
    """
    pretty print data
    """
    pt = PrettyTable(header)
    for dt in data:
        pt.add_row(dt)
    print(pt)
    return pt.get_string()


def str_decode(s):
    """
    decode str
    :param s:
    :return:
    """
    if sys.version_info < (3, 0):
        return s.decode('utf8')

    return s


def color_print(s, color='green'):
    """
    color str
    :param s:
    :param color:
    :return:
    """
    ct = {
        'green': '\033[92m',
        'red': '\033[91m',
        'none': '\033[0m'
    }
    return ''.join([ct[color], s, ct['none']])


def time_now_str(format_str='%Y-%m-%d'):
    """
    获取当天时间
    :param format_str:
    :return:
    """
    return time.strftime(format_str, time.localtime())


def datetime_to_str(dt, format_str='%Y-%m-%d'):
    """
    datetime转换字符串
    :param format_str:
    :param dt:
    :return:
    """
    return dt.strftime(format_str)


def send_mail(ticket_data):
    """
    发送邮件通知
    :param ticket_data:
    :return:
    """
    with open('conf/mail.json', 'r') as f:
        mail_conf = json.loads(f.read())
    receivers = mail_conf['mail_to'].split(';')
    request_date = datetime_to_str(datetime.datetime.now())
    request_date_list = list()
    match_data_list = list()
    nickname_list = list()
    for receiver in receivers:
        request_date_list.append(request_date)
        match_data_list.append(ticket_data)
        nickname_list.append(receiver.split('@')[0])
    # 发送邮件
    sub_vars = {
        'to': receivers,
        'sub': {
            '%nickname%': nickname_list,
            '%ticket_data%': match_data_list,
            '%send_date%': request_date_list
        }
    }
    params = {
        'api_user': const.SEND_CLOUD_API_USER,
        'api_key': const.SEND_CLOUD_API_KEY,
        'template_invoke_name': const.SEND_CLOUD_TEMPLATE_NAME,
        'substitution_vars': json.dumps(sub_vars),
        'from': mail_conf['mail_from'],
        'resp_email_id': 'true',
    }

    r = requests.post(const.SEND_CLOUD_API_URL, data=params)
    res = r.text
    if sys.version_info < (3, 0):
        res = res.encode('utf8')
    response = json.loads(res)
    if response['message'] == 'success':
        return True
    print('send_mail_fail:', r.text)
    return False
