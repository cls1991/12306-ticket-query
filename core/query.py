# coding: utf8

"""
查询核心实现
"""

from util.common import *
from share import const


def query_tickets(from_station, to_station, train_date):
    """
    :param from_station:
    :param to_station:
    :param train_date:
    :return:
    """
    station_names = json.load(open("data/station_name.json", "r"))
    if isinstance(from_station, str):
        from_station = from_station.decode("utf8")
    if isinstance(to_station, str):
        to_station = to_station.decode("utf8")
    from_station_short_cut = station_names[from_station]
    to_station_short_cut = station_names[to_station]
    search_url = const.TICKETS_JSON_URL % (train_date, from_station_short_cut, to_station_short_cut)
    content = json.loads(get_html(search_url, const.USER_AGENT, const.REFER_URL))
    if content["status"] == False:  # query error, return
        return
    data = content["data"]
    rs = list()
    for d in data:
    	dto = d["queryLeftNewDTO"]
    	tmp = dict()
    	tmp["from_station_name"] = dto["from_station_name"]
    	tmp["end_station_name"] = dto["end_station_name"]
    	tmp["qt_num"] = dto["qt_num"]
    	tmp["rw_num"] = dto["rw_num"]
    	rs.append(tmp)
    pp_json(rs)

