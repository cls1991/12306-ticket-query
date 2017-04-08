# coding: utf8

import os
# 切换工作目录到项目根目录
project = os.path.split(os.path.realpath(__file__))[0]
os.chdir(project)

from core.query import query_tickets


def main():
    """
    """
    from_station = "北京"
    to_station = "武汉"
    train_date = "2017-04-08"
    query_tickets(from_station, to_station, train_date)


if __name__ == '__main__':
    main()
