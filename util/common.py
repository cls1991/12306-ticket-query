# coding: utf8

"""
工具集
"""

import re
import json
import pycurl
import time
import datetime
import sys

import requests

if sys.version_info < (3, 0):
    from StringIO import StringIO as BytesIO
else:
    from io import BytesIO

from prettytable import PrettyTable

from share import const

headers = {}
mail_conf = json.load(open("conf/mail.json", "r"))


def header_function(header_line):
    # HTTP standard specifies that headers are encoded in iso-8859-1.
    # On Python 2, decoding step can be skipped.
    # On Python 3, decoding step is required.
    header_line = header_line.decode('iso-8859-1')

    # Header lines include the first status line (HTTP/1.x ...).
    # We are going to ignore all lines that don't have a colon in them.
    # This will botch headers that are split on multiple lines...
    if ':' not in header_line:
        return

    # Break the header line into header name and value.
    name, value = header_line.split(':', 1)

    # Remove whitespace that may be present.
    # Header lines include the trailing newline, and there may be whitespace
    # around the colon.
    name = name.strip()
    value = value.strip()

    # Header names are case insensitive.
    # Lowercase name here.
    name = name.lower()

    # Now we can actually record the header name and value.
    headers[name] = value


def get_html(url, user_agent, refer_url):
    """
    curl html
    :param url:
    :param user_agent:
    :param refer_url:
    :return:
    """
    curl = pycurl.Curl()
    curl.setopt(curl.USERAGENT, user_agent)
    curl.setopt(curl.REFERER, refer_url)

    buffers = BytesIO()
    curl.setopt(curl.SSL_VERIFYPEER, 0)
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEFUNCTION, buffers.write)
    curl.setopt(curl.HEADERFUNCTION, header_function)
    curl.perform()
    curl.close()
    # Figure out what encoding was sent with the response, if any.
    # Check against lowercased header name.
    encoding = None
    if "content-type" in headers:
        content_type = headers['content-type'].lower()
        match = re.search('charset=(\S+)', content_type)
        if match:
            encoding = match.group(1)
            # print('Decoding using %s' % encoding)
    if not encoding:
        # Default encoding for HTML is iso-8859-1.
        # Other content types may have different default encoding,
        # or in case of binary data, may have no encoding at all.
        encoding = 'iso-8859-1'
        # print('Assuming encoding is %s' % encoding)

    body = buffers.getvalue()
    buffers.close()
    # Decode using the encoding we figured out.
    return body.decode(encoding)


def generate_station_name_pairs(use_local_file=True):
    """
    generate snp
    :param use_local_file:
    :return:
    """
    if use_local_file:
        with open("data/station_name.js", "rb") as f:
            sd = f.read().decode('utf8').replace('\n', '')
        rs = dict()
        res = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', sd)
        for r in res:
            rs[r[0]] = r[1]
        if rs:
            with open("data/station_name.json", "wb") as f:
                f.write(json.dumps(rs, indent=4).encode())


def copy_dict_by_keys(s, t, keys):
    """
    copy dict k/v pairs from s to t
    """
    for key in keys:
        if key in s:
            # t[key] = s[key]
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
        return s.decode("utf8")
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


def time_now_str(format_str="%Y-%m-%d"):
    """
    获取当天时间
    :param format_str:
    :return:
    """
    return time.strftime(format_str, time.localtime())


def datetime_to_str(dt, format_str="%Y-%m-%d"):
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
    receivers = mail_conf["mail_to"].split(";")
    request_date = datetime_to_str(datetime.datetime.now())
    request_date_list = list()
    match_data_list = list()
    nickname_list = list()
    for receiver in receivers:
        request_date_list.append(request_date)
        match_data_list.append(ticket_data)
        nickname_list.append(receiver.split("@")[0])
    # 发送邮件
    sub_vars = {
        'to': receivers,
        'sub': {
            "%nickname%": nickname_list,
            "%ticket_data%": match_data_list,
            "%send_date%": request_date_list
        }
    }
    params = {
        "api_user": const.SEND_CLOUD_API_USER,
        "api_key": const.SEND_CLOUD_API_KEY,
        "template_invoke_name": "ticket_query",
        "substitution_vars": json.dumps(sub_vars),
        "from": mail_conf["mail_from"],
        "resp_email_id": "true",
    }

    r = requests.post(const.SEND_CLOUD_API_URL, data=params)
    res = r.text
    if sys.version_info < (3, 0):
        res = res.encode("utf8")
    response = json.loads(res)
    if response['message'] == 'success':
        return True
    print('send_mail_fail:', r.text)
    return False
