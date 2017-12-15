# coding: utf8

"""
系统常量
"""

TICKETS_JSON_URL = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station' \
                   '=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT'

STATION_NAME_JS_URL = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9001'

USER_AGENT = 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) ' \
             'Version/4.0.4 Mobile/7B314 Safari/531.21.10'

REFER_URL = 'https://kyfw.12306.cn'

# SendCloud API
SEND_CLOUD_API_URL = 'http://www.sendcloud.net/webapi/mail.send_template.json'
# SendCloud TEMPLATE_NAME
SEND_CLOUD_TEMPLATE_NAME = 'ticket_query'
# SendCloud API_USER
SEND_CLOUD_API_USER = '$SEND_CLOUD_API_USER'
# SendCloud API_KEY
SEND_CLOUD_API_KEY = '$SEND_CLOUD_API_KEY'
