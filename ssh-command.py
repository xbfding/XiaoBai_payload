#! /usr/bin/env python
# _*_  coding:utf-8 _*_
import argparse
import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='该脚本为ssh执行命令')
    parser.add_argument('ip', type=str, help='目标ip地址')
    parser.add_argument('port', type=int, help='目标端口号')
    parser.add_argument('user', type=str, help='用户名')
    parser.add_argument('passwd', type=str, help='用户密码')
    parser.add_argument('shell', type=str, help='执行的命令')
    args = parser.parse_args()

    print(main.SSHCommond(args.ip, args.port, args.user, args.passwd, args.shell, private_key=None))