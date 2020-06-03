#!/usr/bin/python3.6
#
from box import Box
from common.uploadMirror import start_upload
from verify import gol


def test_function(response):
    print(response)
    return Box({"test_user_name": response.json()["user"]["name"]})

def save_cookie(response):
    #print(response.headers)
    #print(response.content)
    cookies = response.headers.get("Set-Cookie").split()
    des_cookie = "my_id=administrator; LOCALE=zh_CN;"
    for co in cookies:
        #print(co)
        if "JSESSIONID" in co or "cloud" in co:
            tmp_str = " " + co
            des_cookie += tmp_str
    #print(des_cookie)
    return Box({"cookie": des_cookie})

# 用户管理保存ids
def save_zone_ids(response):
    body = response.json()
    ids_dict = response.json().get("rows")[0]
    #获取domainid,删除的时候要用到
    ids = ids_dict.get("domainid")
    zoneName = ids_dict.get("domainname")
    return Box({"ids": ids, "zoneName": zoneName})

def save_cluster_clusterinfo(response):
    body = response.json()
    print(body.get("rows"), "eeeeeeeeeeeeeeeeee")
    try:
        cluster_dict = body.get("rows")[0]
        print(1111111111111111111111111111111111111111)
    except Exception as e:
        #需要增加日志
        return None
    clusterid = cluster_dict.get("clusterid")
    clustername = cluster_dict.get("clustername")
    clusterid_str = ""
    for row in body.get("rows"):
        clusterid_str += ("," + row.get("clusterid"))

    return Box({"clusterid": clusterid, "clusterid_str": clusterid_str, "clustername": clustername})

def save_hostid_str(response):
    ids_list = []
    rows_list = response.json().get("rows")
    print(rows_list, "gg"*20)
    for item in rows_list:
        ids_list.append(item.get("hostid"))
    hostid = ids_list[0]
    ids = ",".join(ids_list)
    print(ids, "f"*20)
    return Box({"ids": ids, "hostid": hostid})

def save_mainStorage_msids(response):
    #json_dict = {"clusterId": "空字段", "logAction": {"async": 1, "id": 1803, "name": ""}}
    #print(response.json())
    mainStorage = response.json().get("rows")[0]
    #for item in mainStorage_list:
        #json_dict["id"] = item.get("msid")
        #json_list.append(json_dict)
    #msids = ",".join(msid_list)
    #print(json_list, "vvvvvvvvvvvvvvvvvvvvvvvvvvv")
    return Box({"msids": mainStorage.get("msid")})

def save_l2network_inf(response):
    info = response.json().get("rows")[0]
    l2networkid = info.get("ltnid")
    l2networkname = info.get("ltnname")
    return Box({"l2networkid": l2networkid, "l2networkname": l2networkname})

def save_calculationSpecifications_inf(response):
    info = response.json().get("rows")[0]
    specid = info.get("specid")
    name = info.get("name")
    return Box({"calcid": specid, "name": name})

def upload_iso():
    body = start_upload()
    return Box({"path": body.get("message"), "url": body.get("message"), "mirrorid": body.get("fileId")})

def save_mirror_inf(response):
    rows = response.json().get("rows")
    inf_dict = {}
    for i in rows:
        if i.get("mformat") == "iso":
            if not inf_dict.get("iso_mirrorid"):
                inf_dict["iso_mirrorid"] = i.get("mirrorid")
                #inf_dict["iso_msid"] = i.get("msid")
        elif i.get("mformat") == "qcow2":
            if not inf_dict.get("qcow2_mirrorid"):
                inf_dict["qcow2_mirrorid"] = i.get("mirrorid")
                #inf_dict["qcow2_msid"] = i.get("msid")
    return Box(inf_dict)

def save_cloudHost_list(response):
    rows = response.json().get("rows")
    gol.set_value("rows", rows)


def get_running_qcow2_vm():
    rows = gol.get_value("rows")
    print(rows)
    for row in rows:
        if row.get("mformat") == "qcow2" and row.get("state") == "running":
            print(row.get("vmid"))
            return Box({"ids": row.get("vmid")})

def get_console_token(response, state="running"):
    rows = response.json().get("rows")
    for row in rows:
        if row.get("state") == state:
            return Box({"console_token": row.get("vmid")})

