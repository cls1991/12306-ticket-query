# coding: utf8

"""
查询核心实现
"""

from util.common import *


def query_tickets(from_station, to_station, train_date, is_subscribe=False):
    """
    :param from_station:
    :param to_station:
    :param train_date:
    :param is_subscribe:
    :return:
    """
    station_names = json.load(open("data/station_name.json", "r"))
    if isinstance(from_station, str):
        from_station = str_decode(from_station)
    if isinstance(to_station, str):
        to_station = str_decode(to_station)
    from_station_short_cut = station_names[from_station]
    to_station_short_cut = station_names[to_station]
    search_url = const.TICKETS_JSON_URL % (train_date, from_station_short_cut, to_station_short_cut)
    try:
        content = json.loads(get_html(search_url, const.USER_AGENT, const.REFER_URL))
        if not content["status"]:  # query error, return
            print("query param error")
            return
        if "data" not in content:
            print("no ticket left")
            return
        data = content["data"]['result']
        station_names_reverse = dict(zip(station_names.values(), station_names.keys()))
        rs = list()
        for d in data:
            t = d.split('|')
            td = [
                t[3],
                station_names_reverse.get(t[4], t[4]),
                station_names_reverse.get(t[7], t[7]),
                t[8],
                t[9],
                format_duration(t[10]),
                t[30],
                t[22],
                t[33],
                t[28],
                t[24],
                t[29],
                t[26],
            ]
            for i, m in enumerate(td):
                if not m:
                    td[i] = '--'
            rs.append(td)
        header = u"车次 出发站 到达站 出发时间 到达时间 历时 一等座 二等座 软卧 硬卧 软座 硬座 无座".split()
        pt = pretty_print(header, rs)
        if is_subscribe:
            send_mail(pt)
    except ValueError:
        print('json decode error')


def format_duration(s):
    """
    format lishi
    :param s:
    :return:
    """
    l = s.replace(':', u'时') + u'分'
    if l.startswith('00'):
        return l[3:]
    return l
