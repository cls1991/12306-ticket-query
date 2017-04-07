# coding: utf8

"""
工具集
"""

import json
import pycurl
from StringIO import StringIO

from prettytable import PrettyTable


def get_html(url, user_agent, refer_url):
    """
    curl html
    :param url:
    :param user_agent:
    :param refer_url:
    :return:
    """
    curl = pycurl.Curl()
    curl.setopt(pycurl.USERAGENT, user_agent)
    curl.setopt(pycurl.REFERER, refer_url)

    buffers = StringIO()
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEDATA, buffers)
    curl.perform()
    body = buffers.getvalue()
    buffers.close()
    curl.close()

    return body


def generate_station_name_pairs(use_local_file=True):
    """
    generate snp
    :param use_local_file:
    :return:
    """
    if use_local_file:
        f = open("data/station_name.js", "rb")
        sl = list()
        for line in f:
            sl.append(line)
        f.close()
        rs = dict()
        sd = ''.join(sl)
        st = sd.split("'")[1]
        for s0 in st.split("@"):
            if s0 == "":
                continue
            s1 = s0.split("|")
            if not s1:
                continue
            for s2 in s1:
                rs[s2] = s1[2]
        if rs:
            f = open("data/station_name.json", "wb")
            f.write(json.dumps(rs))
            f.close()


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
    pt = PrettyTable()
    pt._set_field_names(header)
    for dt in data:
        pt.add_row(dt)
    print(pt)
