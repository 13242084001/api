from box import Box
import json
from common import sshClient
import time
import eventlet
from .gol import *
import requests


def check_login_response_headers(response):
    #print(response.headers)
    #print(2222222222)
    result = False
    if "cloud0" in response.headers.get("Set-Cookie"):
        result = True
    assert result == True

def logout_ok(response):
    pass


def check_stop_py_machine(response):
    #print(json.dumps(response.json()))
    #print(response.json().get("code"), "yyyyyyyyyyyyyyy")
    assert response.json().get("code") == 0

def check_add_role(response):
    body_json = response.json()
    assert body_json.get("code") == 1
    assert body_json.get("error") == None

def check_remove_role(response):
    body = response.json()
    assert body.get("code") == 1
    assert body.get("error") == None

#校验添加区域
def check_add_zone(response):
    body = response.json()
    resourceIds = body.get("resourceIds")
    #print(body)
    assert body.get("code") == 1
    #assert isinstance(resourceIds,list)

def check_query_zone(response):
    body = response.json()
    assert body.get("code") == 1

def check_query_cluster(response):
    body = response.json()
    print("####################################################")
    assert body.get("code") == 1
    assert isinstance(body.get("rows"), list)
#json 校验，暂未使用
def check_cluster_add(response):
    body = response.json()
    print(body)

def check_physicalmachine_query_ok(response):
    body = response.json()
    print(body)
    assert body.get("code") == 1
    #assert body.get("rows")

def check_physical_update_ok(response):
    body = response.json()
    print(body)
    assert body.get("code") == 1
    assert isinstance(body.get("resourceIds"), list)

def check_stop_start_pysicalmachine_ok(response):
    body = response.json()
    assert body.get("code") == 1
    assert isinstance(body.get("resourceIds"), list)

# 校验查询主存储
def check_mainStorage_query_ok(response):
    body = response.json()
    assert body.get("code") == 1
    assert isinstance(body.get("rows"), list)

# 校验修改主存储
def check_mainStorage_update_ok(response):
    body = response.json()
    assert body.get("code") == 1
    assert isinstance(body.get("resourceIds"), list)

# 校验主存储添加集群查询集群列表
def check_query_clusterUnload_list_ok(response):
    body = response.json()
    assert body.get("code") == 1
    assert isinstance(body.get("rows"), list)

# 校验主存储添加集群
def check_mainStorage_addCluster_ok(response):
    assert response.json().get('code') == 1

#校验添加云主机成功
def check_cloudHost_add_ok(response):
    body = response.json()
    print(body)
    assert body.get("code") == 1
    id = body.get("id")
    id_len = len(id.split(","))
    id = id.replace(",", "|")
    username = "root"
    password = "user@dev"
    ip = "172.16.130.252"
    cmd = 'virsh list --all|grep running|grep -E "{0}"|wc -l'.format(id)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret) == id_len:
                #print(1111)
                flag = True
                break
    assert flag

#校验查询running状态的云主机
def check_query_vm_status_ok(response, state):
    #print("zheshi jjjjjj ", state)
    verify_rows = get_value("rows")
    num = 0
    for row in verify_rows:
        if row.get("state") == state:
            num += 1
    local_rows = response.json().get("rows")
    for row in local_rows:
        assert row.get("state") == state
        continue
    assert len(local_rows) == num

def check_query_vm_ok(response, keyword, searchtype):
    searchtype_dict = {0: "name", 2: "hostip"}
    verify_rows = get_value("rows")
    #print(verify_rows,"f"*30)
    num = 0
    for row in verify_rows:
        if keyword in row.get(searchtype_dict.get(searchtype)):
            num += 1
    local_rows = response.json().get("rows")
    for row in local_rows:
        assert keyword in row.get(searchtype_dict.get(searchtype))
        continue
    assert len(local_rows) == num

def search_vmip_list(keyword):
    des_url = "http://172.16.130.254:38080/networkCard/query.do"
    vm_list = get_value("rows")
    #print(vm_list, "8"*10)
    vmid_list = [i.get("vmid") for i in vm_list]
    from common.uploadMirror import login
    result = 0
    cookie = login()
    for vmid in vmid_list:
        params = {
            "order": "asc",
            "offset": 0,
            "limit": 20,
            "vmid": vmid
        }
        res = requests.get(des_url, params=params,
                            headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                     "Cookie": cookie})
        #print(res.json())
        rows = res.json().get("rows")
        for row in rows:
            if keyword in row.get("ip"):
                result += 1
    return result

def check_query_vm_ip_ok(response, keyword):
    cmp_num = search_vmip_list(keyword=keyword)
    rows = response.json().get("rows")
    #print(cmp_num, "hhhhhhh")
    #print(len(rows))
    assert len(rows) == cmp_num

def check_reboot_vm_ok(response):
    assert response.json().get("code") == 1

def check_pause_vm_ok(response):
    vmid = response.json().get("id")
    username = "root"
    password = "user@dev"
    ip = "172.16.130.252"
    cmd = 'virsh list --all|grep pause|grep -E "{0}"|wc -l'.format(vmid)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret):
                # print(1111)
                flag = True
                break
    assert flag

def check_forceStopVM_ok(response):
    vmid = response.json().get("id")
    username = "root"
    password = "user@dev"
    ip = "172.16.130.252"
    cmd = 'virsh list --all|grep shut|grep -E "{0}"|wc -l'.format(vmid)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret):
                # print(1111)
                flag = True
                break
    assert flag