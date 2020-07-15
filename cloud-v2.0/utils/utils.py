#!/usr/bin/python3.6
#
from box import Box
from common.uploadMirror import start_upload, del_iso_splice
from verify import gol
import sys
import pytest
sys.setrecursionlimit(10000000)


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
    # print(rows_list, "gg"*20)
    for item in rows_list:
        ids_list.append(item.get("hostid"))
    hostid = ids_list[0]
    ids = ",".join(ids_list)
    # print(ids, "f"*20)
    return Box({"ids": ids, "hostid": hostid})

def save_mainStorage_msids(response, all=1):
    if all:
        mainStorage = response.json().get("rows")[0]
        return Box({"msids": mainStorage.get("msid"), "clusterid": mainStorage.get("clusterid")})
    else:
        msids = []
        for row in response.json().get("rows"):
            msids.append(row.get("msid"))
        return Box({"msids": ",".join(msids)})

def save_l2network_inf(response):
    rows = response.json().get("rows")
    print(response.json())
    nid_list = []
    l2networkid = l2networkname = ""
    if len(rows) > 1:
        for row in rows:
            nid_list.append(row.get("ltnid"))
            #选择novlan的二层网络
            if 1 == row.get("type"):
                l2networkid = row.get("ltnid")
                l2networkname = row.get("ltnname")
    else:
        nid_list = rows[0].get("ltnid")
        l2networkid = rows[0].get("ltnid")
    print(l2networkid, l2networkname)
    return Box({"l2networkid": l2networkid, "l2networkname": l2networkname, "ids": ",".join(nid_list)})

def save_calculationSpecifications_inf(response):
    info = response.json().get("rows")[0]
    specid = info.get("specid")
    name = info.get("name")
    return Box({"calcid": specid, "name": name})

def upload_iso(iso_type="iso"):
    body, path = start_upload(iso_type)
    del_iso_splice(path)
    return Box({"path": body.get("message"), "url": body.get("message"), "mirrorid": body.get("fileId")})

def save_mirror_inf(response, all=1):
    rows = response.json().get("rows")
    inf_dict = {}
    if all:
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
    else:
        mirrorid_list = []
        for i in rows:
            mirrorid_list.append(i.get("mirrorid"))
        print(mirrorid_list)
        return Box({"ids": ",".join(mirrorid_list)})


def save_cloudHost_list(response):
    rows = response.json().get("rows")
    gol.set_value("rows", rows)
    ids_list = []
    for row in rows:
        ids_list.append(row.get("vmid"))
    return Box({"ids": ",".join(ids_list)})


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
            console_token = row.get("vmid")
            cpunum_add = int(row.get("cpunum") + 2)
            cpunum_cut = int(row.get("cpunum") - 1)
            memorysize = int(row.get("memorysize")/(1024*1024*1024))
            maxmemorysize = int(row.get("maxmemorysize")/1024)
            hostip = row.get("hostip")
            print(memorysize, maxmemorysize)
            if memorysize < maxmemorysize:
                memorysize_modify = memorysize + 1
            else:
                memorysize_modify = memorysize - 1
            memorysize_modify_overflow = maxmemorysize + 1
            return Box({"console_token": console_token, "cpunum_add": cpunum_add, "cpunum_cut": cpunum_cut,
                        "memorysize_modify": memorysize_modify, "memorysize_modify_overflow": memorysize_modify_overflow,
                        "hostip": hostip})

def query_use_or_unuse_cloudDisk(response, use=False):
    rows = response.json().get("rows")
    if use:
        for row in rows:
            if row.get("vmid"):
                return Box({"volumeid": row.get("volumeid"), "vmid": row.get("vmid"), "volname": row.get("name")})
    else:
        for row in rows:
            if not row.get("vmid"):
                return Box({"volumeid": row.get("volumeid"), "hostid": row.get("hostid"), "volname": row.get("name")})

def save_active_ImageServer(response):
    rows = response.json().get("rows")
    for row in rows:
        if row.get("state") == 1:
            return Box({"mirrorid": row.get("msid")})

def choice_no_vm_disk(response, flag=1):
    rows = response.json().get("rows")
    if flag:
        for row in rows:
            if not row.get("vmid"):
                return Box({"volid": row.get("volumeid"), "size": int(row.get("size"))/(1024*1024*1024) + 10,
                            "pmid": row.get("hostid"), "installpath": row.get("installpath"),
                            "pmip": row.get("hostip"), "msid": row.get("msid")})
    else:
        for row in rows:
            if row.get("vmid"):
                return Box({"volid": row.get("volumeid"), "vmid": row.get("vmid")})


def get_not_ha_vm(response, level=1):
    rows = response.json().get("rows")
    for row in rows:
        if int(row.get("vmlevel")) == level:
            return Box({"vmid": row.get("vmid")})


def choice_mirrorSever(response):
    rows = response.json().get("rows")
    for row in rows:
        if 1 == row.get("state"):
            return Box({"mirrorid": row.get("msid")})


def choice_iso_mirror(response):
    rows = response.json().get("rows")
    for row in rows:
        if row.get("mformat") == "iso" and row.get("status") == 1:
            return Box({"mirrorid": row.get("mirrorid")})


def get_stopped_and_qcow2_vm(response, mformat):
    rows = response.json().get("rows")
    for row in rows:
        if row.get("state") == "stopped" and row.get("mformat") == mformat:
            return Box({"vmid": row.get("vmid"), "rootvolumeid": row.get("rootvolumeid"), "hostip": row.get("hostip")})

def save_snapshots_list(response):
    rows = response.json()
    snapshotid =  rows[0].get("snapshotid")
    volumeid = rows[0].get("volumeid")
    snapname = rows[0].get("name")
    return Box({"snapshotid": snapshotid, "volumeid": volumeid, "snapname": snapname})


def save_all_cloudDisk_list(response):
    rows = response.json().get("rows")
    disk_list = []
    for row in rows:
        disk_list.append(row.get("volumeid"))
    return Box({"ids": ",".join(disk_list)})


def save_all_deleteVM(response):
    rows = response.json().get("rows")
    id_list = []
    for row in rows:
        id_list.append(row.get("vmid"))
    return Box({"ids": ",".join(id_list)})


def save_all_cloudDiskSpecId(response):
    rows = response.json().get("rows")
    id_list = []
    for row in rows:
        id_list.append(row.get("specid"))
    return Box({"ids": ",".join(id_list)})

def save_l3pri_id_list(response):
    rows = response.json().get("rows")
    id_list = []
    for row in rows:
        id_list.append(row.get("nid"))
    return Box({"ids": id_list})


def save_vxlan_clusterid_list(response):
    vxlan_clusterid_list = []
    rows = response.json().get("rows")
    try:
        for row in rows:
            vxlan_clusterid_list.append(row.get("clusterid"))
        return Box({"vxlan_clusterid_list": ",".join(vxlan_clusterid_list)})
    except Exception as e:
        print(e)
        return Box({"vxlan_clusterid_list": []})

def calc_vxlan_vni(vnistart, endvni=0, flag=0):
    import random
    if flag:
        return {"vni": random.randint(int(vnistart), int(endvni))}
    else:
        return {"vni": int(endvni) + 1}


def calc_vxlan_vni_range(flag, vnistart, endvni):
    import random
    if 1 == flag:
        if not (vnistart and endvni):
            return {"vnistart": 1, "endvni": 100}
        return {"vnistart": random.randint(int(vnistart), int(endvni)), "endvni": int(endvni) + 1}
    elif 2 == flag:
        return {"vnistart": int(endvni), "endvni": int(endvni) + 1}
    elif 3 == flag:
        return {"vnistart": (int(endvni) + 2), "endvni": (2**24 - 2)}


def save_vxlan_pool_info(response):
    rows = response.json().get("rows")
    ids = []
    for row in rows:
        print(row.get("vxlanpoolname"))
        if "3" not in row.get("vxlanpoolname"):
            ids.append(row.get("vxlanpoolid"))
    return Box({"vxlan_pool_ids": ",".join(ids)})


def save_vxlanNet_vni_list(response):
    rows = response.json().get("rows")
    vni_list = []
    for row in rows:
        vni_list.append(row.get("vni"))
    return Box({"vni_list": ",".join(vni_list)})


def choice_network_type_to_add_vm(response, flag, index=1):
    assert isinstance(list, response.json().get("rows"))
    nid_list = []
    for row in response.json().get("rows"):
        if int(flag) == row.get("networktype"):
            nid_list.append(row.get("nid"))

        elif 21 == int(flag) and 2 == row.get("networktype"):
            nid_list.append(row.get("nid"))
        elif 21 == int(flag) and 2 == row.get("networktype"):
            nid_list.append(row.get("nid"))

    return Box({"l3networkid": nid_list[int(index) - 1]})


def save_l3network_mtu(response):
    rows = response.json().get("rows")
    if not rows:
        pytest.skip("没有三层网络！")
    else:
        nid = rows[0].get("nid")
        mtu = int(rows[0].get("mtu")) + 10
        pnname = rows[0].get("pnname")
        return Box({"nid": nid, "mtu": mtu, "pnname": pnname})


def choice_vpc_memory(response):
    memory = int(response.json().get("rows")[1].get("memory")) /1024 - 1
    return Box({"memory": memory})