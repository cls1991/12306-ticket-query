# coding: utf8

import os

from core.query import query_tickets

# 切换工作目录到项目根目录
project = os.path.split(os.path.realpath(__file__))[0]
os.chdir(project)


def main():
    """
    test main
    """
    from_station = '北京'
    to_station = '武汉'
    train_date = '2017-12-16'
    query_tickets(from_station, to_station, train_date, is_subscribe=True)


if __name__ == '__main__':
    main()
