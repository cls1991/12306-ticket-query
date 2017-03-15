# coding: utf8

"""
查询核心实现
"""

import json

from util.common import *
from share import const


def query_tickets(from_station, to_station, train_date):
	"""
	:param from_station:
	:param to_station:
	:param train_date:
	:return:
	"""
	search_url = const.TICKETS_JSON_URL % (train_date, from_station, to_station)
	content = json.loads(get_html(search_url, const.USER_AGENT, const.REFER_URL))
	data = content["data"]
	pp_json(data)

