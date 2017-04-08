# coding: utf8

"""
工具集
"""

import re
import json
import pycurl
import sys

if sys.version_info < (3, 0):
    from StringIO import StringIO as BytesIO
else:
    from io import BytesIO

from prettytable import PrettyTable

headers = {}


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
