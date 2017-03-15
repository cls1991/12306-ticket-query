# coding: utf8

"""
系统常量
"""

PASSAGER_TYPE_ENUM = {1:"ADULT", 2:"0X00"}

### for example
# https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-03-16&leftTicketDTO.from_station=BJP \
# &leftTicketDTO.to_station=WHN&purpose_codes=ADULT
###

TICKETS_JSON_URL = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s& \
leftTicketDTO.to_station=%s&purpose_codes=ADULT"

STATION_NAME_JS_URL = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9001"

USER_AGENT = 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) ' \
             'Version/4.0.4 Mobile/7B314 Safari/531.21.10'

REFER_URL = 'https://kyfw.12306.cn'

