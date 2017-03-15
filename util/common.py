# coding: utf8

"""
工具集
"""

import json
import pycurl
# import certifi
from StringIO import StringIO


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
    # curl.setopt(pycurl.CAINFO, certifi.where())
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEDATA, buffers)
    curl.perform()
    body = buffers.getvalue()
    buffers.close()
    curl.close()

    return body


def pp_json(jdata, sort=True, indents=4):
	"""
	pretty print json data
	"""
	print(json.dumps(jdata, sort_keys=sort, indent=indents))
