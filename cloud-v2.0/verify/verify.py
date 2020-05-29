from box import Box
import json

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

def check_cloudHost_add_ok(response):
    body = response.json()
    print(body)
    assert body.get("code") == 1

