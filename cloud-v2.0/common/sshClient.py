#import yaml
#import os
import time
import paramiko
from paramiko import AuthenticationException
from paramiko.ssh_exception import NoValidConnectionsError
#import threading
#import logging

#logger = logging.getLogger()
#logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s", filename="./ssh.log", filemode="w")
#logger.format = "%(levelname)s:%(message)s"
"""
def readConfig():
    #yamlPath = os.path.join(curPath, "config.yaml")
    try:
        with open("./config.yaml", "r", encoding="utf-8") as f:
            data = f.read()
        #logging.info("读取配置文件内容:%s" % (data,))
    except Exception as e:
        print(str(e))
        #logging.error("没有配置文件! %s" % str(e))
        os._exit(0)
    d = yaml.load(data)
    return d
"""
def tunction(ip,username,password,cmd):
    client = paramiko.SSHClient()
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #print(ip, username, password, type(ip), type(username), type(password))
        client.connect(ip,username=username, password=password)
    except AuthenticationException:
        #logging.warning("username or password error!" % (ip,))
        print("#"*30)
        print("%s username or password error!" % (ip,))
        return False
    except NoValidConnectionsError:
        #logging.warning("%s connect time out!" % (ip,))
        #print("#"*30)
        print("%s connect time out" % (ip,))
        return False
    #logging.info("正在登录%s..." %ip)
    out = None
    while 1:
        time.sleep(1)
        try:
            stdin,stdout,stdeer = client.exec_command(cmd)
        except AttributeError:
            #logging.warning("%s is not exists host!" % (ip,))
            continue
        #logging.info("正在%s上执行命令" % ip)
        #print(stdout.read())
        print(cmd)
        out, err = stdout.read(), stdeer.read()
        print(out)
        print(err)
        if out:
            print("check ok!")
            #print("\033[1;36;40m设备%s执行成功\033[0m" % (ip,))
            #print("%s is exec ok" % (ip,))
            #logging.info("\033[1;36;40m设备 %s 执行成功, %s\033[0m" % (ip, ",".join(stdout)))
            #print("#"*30)
            #print(stdout.read())
            #time.sleep(0.1)
            break
        else:
            #logging.error("\033[1;31;40m设备%s执行失败,%s\033[0m" % (ip, ",".join(stdeer)))
            #print("\033[1;31;40m设备%s执行失败\033[0m" % (ip,))
            print("%s exec not ok! " % (ip,))
            return None
    client.close()
    return out

"""
def main(**kwargs):
    #字典是无序的
    #ip_list, username, password, cmd = kwargs.values()
    ip_list = kwargs.get("ip_list")
    username = kwargs.get("username")
    password = str(kwargs.get("password"))
    cmd = kwargs.get("cmd")
    #logging.debug("等待登录的设备列表: %s" % (ip_list,))
    thread_list = []
    for ip in ip_list:
        t = threading.Thread(target = tunction,args = (ip,username,password,cmd))
        thread_list.append(t)
    for th in thread_list:
        th.start()
    for th in thread_list:
        th.join()
"""
if __name__ == "__main__":
    """
    start_time = time.time()
    d = readConfig()
    m = threading.Thread(target = main,kwargs = d)
    m.setDaemon(True)
    m.start()
    m.join()
    end_time = time.time()
    chg_time = str(start_time - end_time) + "s"
    print(chg_time)
    """
    pass