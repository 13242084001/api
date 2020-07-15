import pytest
from common.sshClient import tunction
from box import Box

def pytest_collection_modifyitems(config, items):
    items.sort(key=lambda x: x.name)
    #print("after: %s", items)


@pytest.fixture
def calc_l2vmn_number():
    username = "root"
    password = "user@dev"
    ip = "172.16.130.254"
    cmd = "kubectl get vmn|grep l2network|wc -l"
    try:
        l2vmn_num = tunction(ip=ip, username=username, password=password, cmd=cmd)
        l2vmn_num = int(l2vmn_num)
    except Exception:
        l2vmn_num = 0
    #print(l2vmn_num, 'kkkkkkkkkkkkkkkkkk')
    return l2vmn_num