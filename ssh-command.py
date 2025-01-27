#! /usr/bin/env python3
# _*_  coding:utf-8 _*_
import argparse
import paramiko

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='该脚本为ssh执行命令')
    parser.add_argument('ip', type=str, help='目标ip地址')
    parser.add_argument('port', type=int, help='目标端口号')
    parser.add_argument('user', type=str, help='用户名')
    parser.add_argument('passwd', type=str, help='用户密码')
    parser.add_argument('shell', type=str, help='执行的命令')
    args = parser.parse_args()

    print(SSHCommond(args.ip, args.port, args.user, args.passwd, args.shell, private_key=None))
