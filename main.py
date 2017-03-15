# coding: utf8

import os
# 切换工作目录到项目根目录
project = os.path.split(os.path.realpath(__file__))[0]
os.chdir(project)

from core.query import query_tickets


if __name__ == '__main__':
    # 测试用例
    if __name__ == '__main__':
    	from_station = "BJP"
    	to_station = "WHN"
    	train_date = "2017-03-16"
        query_tickets(from_station, to_station, train_date)

