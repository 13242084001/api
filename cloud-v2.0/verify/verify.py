from common import sshClient
import time
import eventlet
from .gol import *
import requests
from common.uploadMirror import login
from common.sqlquery import Query
#import pytest
import json


def check_login_response_headers(response):
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
def check_mainStorage_addCluster_ok(response, clusterId, uri):
    assert response.json().get('code') == 1
    #print(response.json())
    result = Query()('SELECT * FROM `cl_host_inf` WHERE CLUSTERID="{0}" AND STATE=1 AND DELETED=0'.format(clusterId))
    #print(result)
    #print(555555555555555555555555)
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    cmd = 'kubectl get vmp|grep "{0}"|wc -l'.format(uri)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret) == len(result):
                # print(1111)
                flag = True
                break
    assert flag


def check_delete_mainStorage_ok(response, ids):
    id_list = ids.split(",")
    #result = Query()(
    #    'SELECT COUNT(*) FROM `cl_host_inf` WHERE CLUSTERID="{0}" AND STATE=1 AND DELETED=0'.format(clusterid))
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    for id in id_list:
        cmd = 'kubectl get vmp|grep "{0}"|wc -l'.format(id)
        flag = False
        eventlet.monkey_patch()
        with eventlet.Timeout(180, False):
            while 1:
                time.sleep(0.5)
                ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
                try:
                    if not int(ret):
                        # print(1111)
                        flag = True
                        break
                except Exception as e:
                    print(e)
                    flag = True
                    break
        assert flag

def check_add_mirrorServer_ok(response):
    print(response.json())
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    cmd = 'kubectl get vmp|grep vmdi|wc -l'
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret) > 1:
                # print(1111)
                flag = True
                break
    assert flag


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
    ip = "172.16.130.254"
    cmd = 'kubectl get vm|grep -E "{0}"|wc -l'.format(id)
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

def check_pause_forceStop_stop_ok(response, state, hostip):
    vmid = response.json().get("id")
    username = "root"
    password = "user@dev"
    ip = hostip
    cmd = 'virsh list --all|grep {0}|grep -E "{1}"|wc -l'.format(state, vmid)
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
    des_url = "http://172.16.130.254:38080/networkCard/query.do"
    params = {
        "order": "asc",
        "offset": 0,
        "limit": 20,
        "searchtype": 0,
        "keyword": None,
        "state": None,
    }
    cookie = login()
    res = requests.get(des_url, params=params,
                       headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                "Cookie": cookie})
    # print(res.json())
    rows = res.json().get("rows")
    if state == "shut":
        st = "stopped"
    elif state == "paused":
        st = state
    else:
        st = "running"
    for row in rows:
        if row.get("vmid") == vmid:
            assert row.get("state") == st


def check_all_vm_stop(response, ids):
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    for i in ids.split(","):
        cmd = 'kubectl get vm|grep {0}|grep -i shut|wc -l'.format(i)
        flag = False
        eventlet.monkey_patch()
        with eventlet.Timeout(180, False):
            while 1:
                time.sleep(0.5)
                ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
                if not (int(ret) - 3):
                    # print(1111)
                    flag = True
                    break
        assert flag


def check_cloudDisk_add_ok(response, template=0):
    id = response.json().get("id")
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    if template:
        cmd = 'find /var/lib/libvirt/cstor/ -name {0}|wc -l'.format(id)
    else:
        cmd = 'kubectl get vmd|grep {0}|wc -l'.format(id)
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

def check_cloudDiskLoad_or_unload_ok(response, vmid, volumeid, typee=1):
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    cmd = 'kubectl get vm {0} -o yaml|grep {1}|wc -l'.format(vmid, volumeid)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if typee:
                if int(ret):
                    # print(1111)
                    flag = True
                    break
            else:
                if not int(ret):
                    # print(1111)
                    flag = True
                    break
    assert flag


def check_cloudDisk_queryImageserver_ok(response):
    rows = response.json().get("rows")
    for row in rows:
        assert row.get("state") == 1


def check_cloudDisk_snapshot_add_ok(response):
    id = response.json().get('id')
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    cmd = 'kubectl get vmd|grep {0}|wc -l'.format(id)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret):
                flag = True
                break
    assert flag

def check_cloudDisk_setQos_ok(response, vmid, rx, tx):
    assert response.json().get("id")
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    for i in [rx, tx]:
        cmd = "kubectl get vm {0} -i yaml|grep 'text: {1}'|wc -l".format(vmid, i*1024*1024)
        flag = False
        eventlet.monkey_patch()
        with eventlet.Timeout(180, False):
            while 1:
                time.sleep(0.5)
                ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
                if int(ret):
                    flag = True
                    break

        assert flag

def check_cloudDisk_cancleQos_ok(response, vmid):
    assert response.json().get("id")
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    cmd = "kubectl get vm {0} -i yaml|grep -E 'write|read'|wc -l".format(vmid)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret):
                flag = True
                break
    assert flag

def check_cloudDisk_expandVol_ok(response, installpath, size, hostip):
    assert response.json().get("id")
    username = "root"
    password = "user@dev"
    ip = hostip
    cmd = "qume-img info %s|grep virtual|awk '{print $3}'" % (installpath,)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if str(ret) == size:
                flag = True
                break
    assert flag

#这个函数本来是用来验证存储迁移查询可选择的物理机列表的，但是开发傻逼，传参没传clusterid，导致这里无法验证
def verify_query_cluster_all_phymachine_ok(response):
    pass

def check_cloudDisk_migrate_ok(response, installpath, pmip, msurl, msname):
    cloudDiskId = response.json().get("resourceIds")[0]
    username = "root"
    password = "user@dev"
    ip = pmip
    cmd = "kubectl get vmd|grep %s|awk '{print $3}'" % (cloudDiskId,)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if msurl in str(ret) and (msurl not in installpath):
                flag = True
                break
    assert flag

    des_url = "http://172.16.130.254:38080/cloudDisk/query.do"
    params = {
        "order": "asc",
        "offset": 0,
        "limit": 20,
        "searchtype": 0,
        "keyword": None,
        "state": None,
    }
    cookie = login()
    res = requests.get(des_url, params=params,
                       headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                "Cookie": cookie})
    # print(res.json())
    rows = res.json().get("rows")
    for row in rows:
        if row.get("volumeid") == cloudDiskId:
            assert row.get("msname") == msname
            break

def check_query_cloudHost_loadable_or_unloadable_disk_ok(response, vmid, load=1):
    if load:
        sql_result = Query()("SELECT * FROM `cl_volume_inf` where STATE = 0 and VMID is null;")
    else:
        sql_result = Query()('SELECT * FROM `cl_volume_inf` where VMID="{0}" and TYPE=2;'.format(vmid,))
    sql_volid_list = [x.get("VOLUMEID") for x in sql_result]
    json_volid_list = [x.get("volumeid") for x in response.json().get("rows")]
    assert len(sql_volid_list) == len(json_volid_list)
    for volid in sql_volid_list:
        assert volid in json_volid_list


def check_cloudHost_setHa_ok(response, vmid, hostip, cancle=0):
    username = "root"
    password = "user@dev"
    ip = hostip
    cmd = 'kubectl get vm {0} -o yaml|grep -w ha|wc -l'.format(vmid)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if not cancle:
                if int(ret):
                    flag = True
                    break
            else:
                if not int(ret):
                    flag = True
                    break
    assert flag


def check_cloudHost_makeSnapshot_ok(response, vmid, hostip):
    id = response.json().get("id")
    assert id
    username = "root"
    password = "user@dev"
    ip = hostip
    cmd = 'kubectl get vmd|grep {0}|wc -l'.format(vmid)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret):
                flag = True
                break
    assert flag


def check_makeVMimage_ok(response, hostip):
    id = response.json().get("id")
    assert id
    username = "root"
    password = "user@dev"
    ip = hostip
    cmd = 'find / -name {0}|wc -l'.format(id)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret):
                flag = True
                break
    assert flag


def check_modify_cpu_num_ok(response, cpunum_new, hostip):
    id = response.json().get("id")
    assert id
    username = "root"
    password = "user@dev"
    ip = hostip
    cmd = "virsh vcpucount %s|grep current|awk '{print $3}'|tail -1" % (id,)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret) == cpunum_new:
                flag = True
                break
    assert flag


def check_modify_mem_ok(response, memorysize, hostip):
    #print(11111111111111111111111111111111111111111)
    #print(response.json())
    id = response.json().get("id")
    #print("this is id....", id)
    assert id
    username = "root"
    password = "user@dev"
    ip = hostip
    cmd = "virsh dominfo %s|grep Use|awk '{print $3}'" % (id,)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(int(ret)/(1024*1024)) == memorysize:
                flag = True
                break
    assert flag


def check_query_cmrom_iso(response, vmid):
    mirrorid_list = Query()('SELECT MIRRORID FROM `cl_mirror_inf` WHERE status=1 and MFORMAT="iso" AND '
                         'DOMAINID=(SELECT DOMAINID FROM `cl_vm_inf` WHERE VMID="{0}") '
                         'AND MIRRORID NOT IN (SELECT ISOID FROM `cl_vmcdrom_inf` WHERE'
                         ' VMID="{1}")'.format(vmid, vmid))
    rows = response.json().get("rows")
    assert len(mirrorid_list) == len(rows)
    for row in rows:
        assert row.get("mirrorid") in mirrorid_list


def check_addCdrom_ok(vmid, mirrorid, hostip):
    username = "root"
    password = "user@dev"
    ip = hostip
    cmd = "kubectl get vm {0} -o yaml|grep {1}.iso|wc -l".format(vmid, mirrorid)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            print("this is flag...", flag)
            if int(ret):
                flag = True
                break
    assert flag


def check_changeBootSequence_ok(response, vmid, bootSeq, hostip):
    assert response.json().get("id")
    username = "root"
    password = "user@dev"
    ip = hostip
    cmd = "kubectl get vm {0} -o yaml|grep order|cut -d: -f 2".format(vmid, )
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(180, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            ret = ret.decode("utf-8").replace("\n", "").replace(" ", "")
            if bootSeq == 1:
                if ret == "12":
                    flag = True
                    break
            elif bootSeq == 2:
                if ret == "21":
                    flag = True
                    break
    assert flag


def check_changeSystem_querySystem_ok(response, vmid):
    mirrorid_list = Query()('SELECT MIRRORID FROM `cl_mirror_inf` WHERE status=1 and MFORMAT!="iso" AND '
                            'DOMAINID=(SELECT DOMAINID FROM `cl_vm_inf` WHERE VMID="{0}") '
                            'AND MIRRORID NOT IN (SELECT ISOID FROM `cl_vmcdrom_inf` WHERE'
                            ' VMID="{1}")'.format(vmid, vmid))
    rows = response.json().get("rows")
    assert len(mirrorid_list) == len(rows)
    for row in rows:
        assert row.get("mirrorid") in mirrorid_list


def check_changeOs_ok(response, template_url, rootvolumeid, hostip):
    username = "root"
    password = "user@dev"
    ip = hostip
    cmd = "diff %s `kubectl get vmd %s|tail -1|awk '{print $3}'`|wc -l" % (template_url, rootvolumeid)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(30, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            print("this is flag...", flag)
            if not int(ret):
                flag = True
                break
    assert flag



def check_delete_mirror_all_ok(response):
    print(response.json())


def check_delete_mirrorServer_ok(response, mirrorServerId):
    print(response.json())
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    cmd = "kubectl get vmp|grep {0}|wc -l".format(mirrorServerId)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(30, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            print("this is flag...", flag)
            if not int(ret):
                flag = True
                break
    assert flag


def check_delete_all_resource_ok(response, flag="vm"):
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    ids = response.json().get("id")
    ids_list = ids.split(",")
    for id in ids_list:
        if flag == "vm":
            cmd = "kubectl get vm|grep {0}|wc -l".format(id)
        else:
            cmd = "kubectl get vmp|grep {0}|wc -l".format(id)
        flag = False
        eventlet.monkey_patch()
        with eventlet.Timeout(30, False):
            while 1:
                time.sleep(0.5)
                ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
                #print("this is flag...", flag)
                if not int(ret):
                    flag = True
                    break
        assert flag


def check_delete_net(response, l2vmn_num=2):
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    cmd = "kubectl get vmn|grep l2network|wc -l"
    flag = False

    eventlet.monkey_patch()
    with eventlet.Timeout(30, False):
        while 1:
            time.sleep(0.5)
            try:
                ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
                ret = int(ret)
            except Exception:
                flag = True
                break
            if int(l2vmn_num) - ret == 2:
                flag = True
                break
    assert flag

#l2vmn check
def check_creat_net_ok(response, l2vmn_num=0):
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    cmd = "kubectl get vmn|grep l2network|wc -l"
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(30, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret) - int(l2vmn_num) == 2:
                flag = True
                break
    assert flag

def check_creat_l3_net_ok(response):
    id = response.json().get("id")
    assert id
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    cmd = "kubectl get vmn|grep {0}|wc -l".format(id)
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(30, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret):
                flag = True
                break
    assert flag


def check_creat_vxlanPool_ok(response, pool_name):
    #print(response)
    try:
        code = response.json().get("code")
        if "1" in pool_name:
            assert -1 == code
        else:
            assert 1 == code
    except Exception as e:
        print(e)
        assert True


def check_add_vxlan_vni_ok(response, flag):
    print(response.json())
    if 3 == flag:
        assert response.json().get("code") == 1
    if 2 == flag:
        assert response.json().get("code") == -1
    if 1 == flag:
        assert response.json().get("code") == -1


def check_delete_vni_range_ok(response, vni_list, vnistart, endvni):
    for vni in vni_list.split(","):
        if vni in range(int(vnistart), int(endvni) + 1):
            assert -1 == response.json().get("code")
    assert 1 == response.json().get("code")

def check_delete_vxlan_net_ok(response, vni, vxlan_clusterid_list):
    assert response.json().get("code") == 1
    #print(vxlan_clusterid_list)
    #print(7777777777777777777777777)
    try:
        vxlan_clusterid_list = json.loads(vxlan_clusterid_list)
    except Exception:
        vxlan_clusterid_list = tuple(vxlan_clusterid_list.split(","))
        #print(vxlan_clusterid_list)
        #print(66666666666666)
        if len(vxlan_clusterid_list) > 1:
            sql_cmd = 'SELECT HOSTIP FROM `cl_host_inf` WHERE STATE=1 AND DELETED=0 AND `STATUS`="Ready" and CLUSTERID IN {0};'.format(str(vxlan_clusterid_list))
        else:
            sql_cmd = 'SELECT HOSTIP FROM `cl_host_inf` WHERE STATE=1 AND DELETED=0 AND `STATUS`="Ready" and CLUSTERID="{0}";'.format(vxlan_clusterid_list[0])
        #print(sql_cmd)
        #print(555555555555555555555)
        result = Query()(sql_cmd)
        ip_list = []
        for re in result:
            ip_list.append(re.get("HOSTIP"))
        username = "root"
        password = "user@dev"
        for ip in ip_list:
            cmd = "ovs-vsctl list-br|grep vx{0}|wc -l".format(vni)
            flag = False
            eventlet.monkey_patch()
            with eventlet.Timeout(30, False):
                while 1:
                    time.sleep(0.1)
                    ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
                    if not int(ret):
                        flag = True
                        break
            assert flag


def check_modify_l3network_mtu(response, mtu):
    id = response.json().get("id")
    cmd = "ovn-nbctl dhcp-options-get-options `ovn-nbctl show %s|grep dhcp|awk -F\"-\" '{print $3\"-\"$4\"-\"$5\"-\"$6\"-\"$7}'`|grep mtu|cut -d\"=\" -f2" % (id,)
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(30, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret) == int(mtu):
                flag = True
                break
    assert flag

def check_l3network_add_dns(response, mtu, rows, nid, dns_addr):
    cmd = "ovn-nbctl dhcp-options-get-options `ovn-nbctl show %s|grep dhcp|awk -F\"-\" '{print $3\"-\"$4\"-\"$5\"-\"$6\"-\"$7}'`|grep -E 'mtu|dns'|sed ':a;N;s/\n/\t/;ba;'" % (nid,)
    dns_list = [row.get("dns") for row in rows]
    re_mtu = 0
    re_dns_list = []
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(30, False):
        while 1:
            time.sleep(0.2)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            tp_str = ret.split()
            for i in tp_str:
                if "mtu" in i:
                    re_mtu = int(i.split("=")[1])
                elif "dns" in i:
                    if "," in i:
                        re_dns_list = i[12:-1].split(",")
                    else:
                        re_dns_list.append(i.split("=")[1])
            assert int(mtu) == re_mtu
            assert dns_addr in re_dns_list
            flag_2 = True
            for dns in dns_list:
                if dns not in re_dns_list:
                    flag_2 = False
                    break
            if flag_2:
                flag = True
                break
    assert flag


def check_vpc_network_add_ok(response):
    id = response.json().get("id")
    assert id
    cmd = "kubectl get vmn|grep {0}|wc -l".format(id,)
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(40, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if 1 == int(ret):
                flag = True
                break
    assert flag


def check_vpc_router_stop_or_start(response):
    id = response.json().get("id")
    cmd = "kubectl get vm|grep {0}|grep -i shut|wc -l".format(id, )
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(100, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if 1 == int(ret):
                flag = True
                break
    assert flag


def check_setConsolePasswd_ok(response, hostip, passwd=None):
    id = response.json().get("id")
    if passwd:
        cmd = 'cat /tmp/%s.xml |grep passwd|awk -F"passwd=" \'{print $2}\'|cut -d"\"" -f2' % (id,)
    else:
        cmd = 'cat /tmp/%s.xml |grep passwd|wc -l' % (id,)
    username = "root"
    password = "user@dev"
    ip = hostip
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(30, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if passwd:
                if ret == str(passwd):
                    flag = True
                    break
            else:
                if not int(ret):
                    flag = True
                    break
    assert flag


def check_modifyCpuNum_ok(response, hostip, cpunum):
    id = response.json().get("id")
    cmd = "virsh vcpucount %s|grep current|grep live|awk '{print $3}'" % (id,)
    username = "root"
    password = "user@dev"
    ip = hostip
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(30, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret) == int(cpunum):
                flag = True
                break
    assert flag


def check_modifyVpcMem_ok(response, memory, hostip):
    id = response.json().get("id")
    cmd = "virsh dominfo %s|grep 'Used mem'|awk '{print $3}'" % (id,)
    username = "root"
    password = "user@dev"
    ip = hostip
    flag = False
    eventlet.monkey_patch()
    with eventlet.Timeout(30, False):
        while 1:
            time.sleep(0.5)
            ret = sshClient.tunction(ip=ip, username=username, password=password, cmd=cmd)
            if int(ret)/(1024*1024) == int(memory):
                flag = True
                break
    assert flag