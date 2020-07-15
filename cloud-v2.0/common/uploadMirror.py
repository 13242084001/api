#!/usr/bin/env python3.6
#
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import requests
import time
import hashlib
import os
import shutil


global_url = "http://172.16.130.254:38080"
upload_url = global_url + "/largefile/upload"
check_url = global_url + "/largefile/mergeOrCheckChunks.do"
data = {"userId": "administrator", "password": "9DyrH0qty0SqrdsvVCjnJQ==", "userType": 0, "loginType": 1}

def login():
    r = requests.post(global_url + "/login.do", verify=False, data=data)
    #print(r.headers)
    cookies = r.headers.get("Set-Cookie").split()
    des_cookie = "my_id=administrator; LOCALE=zh_CN;"
    for co in cookies:
        # print(co)
        if "JSESSIONID" in co or "cloud" in co:
            tmp_str = " " + co
            des_cookie += tmp_str
    return des_cookie

#获取chunk上传进度条
def my_callback(monitor):
    progress = (monitor.bytes_read / monitor.len) * 100
    print("\r 文件上传进度：%d%%(%d/%d)"
          % (progress, monitor.bytes_read, monitor.len), end=" ")

#计算iso文件的MD5值
def get_file_md5(fname):
    m = hashlib.md5()   #创建md5对象
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  #更新md5对象
    return m.hexdigest()    #返回md5对象



#print(file_md5)

#print(chunkSize)
count = 0
#切割大文件
def cut_big_file(file_path, file_name):
    global count
    file_size = 50 * 1024 * 1024
    eof = False
    with open(file_path + file_name, 'rb') as f_source:
        file_path = file_path + "tmp\\"
        while True:
            f_source.seek(file_size * count, 0)
            chunk_data = f_source.read(file_size)
            if len(chunk_data) < file_size:
                eof = True
            with open("{0}{1}.iso".format(file_path, count), 'wb+') as f_dest:
                #print("creating {0} file".format(count))
                f_dest.write(chunk_data)
                count += 1
            if eof:
                print("file cut finished\n")
                return


def del_iso_splice(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_iso_splice(c_path)
        else:
            os.remove(c_path)

def start_upload(iso_type="iso"):
    if iso_type == "qcow2":
        file_name = r"CentOS-7-x86_64-Minimal-2003.iso"
        file_path = r"C:\Users\lq\Desktop\api\api\cloud-v2.0\common" + "\\"
    elif iso_type == "route_qcow2":
        file_name = r"vyos-agent.qcow2"
        file_path = r"C:\Users\lq\Desktop\api\api\cloud-v2.0\common" + "\\"
    else:
        file_name = r"CentOS-7-x86_64-Minimal-2003.iso"
        file_path = r"C:\Users\lq\Desktop\api\api\cloud-v2.0\common" + "\\"
    des_cookie = login()
    # 获取iso文件大小
    chunkSize = os.path.getsize(file_path + file_name)
    file_md5 = get_file_md5(file_path + file_name)
    cut_big_file(file_path, file_name)
    file_path = file_path + "tmp\\"
    for i in range(0, count):
        params = {
            "param": "checkChunk",
            "fileName": file_name,
            "fileMd5": file_md5,
            "chunk": i,
            "chunkSize": chunkSize
        }
        res = requests.post(check_url, params=params,
                            headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                     "Cookie": des_cookie})
        print(res.text)
        e = MultipartEncoder(fields={'file': (file_name, open(file_path + str(i) + ".iso", 'rb'), 'application/octet-stream'), "fileMd5": file_md5, "chunk": str(i)
                                    })
        m = MultipartEncoderMonitor(e, my_callback)
        r = requests.post(upload_url, data=m, headers={'Cookie': des_cookie, "Content-Type": e.content_type})

    params = {
        "param": "mergeChunks",
        "fileName": file_name,
        "fileMd5": file_md5
    }

    re = requests.post(check_url, params=params, headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Cookie":des_cookie})
    #print(re.text)
    if re.json().get("success"):
        time.sleep(5)
        #del_iso_splice(file_path)
        return re.json(), file_path
    return False

if __name__ == "__main__":
    if start_upload():
        print("upload iso success!")
    else:
        print("upload iso fail!")