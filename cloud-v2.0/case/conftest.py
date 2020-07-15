#coding="utf-8"
import pytest
import logging.config
import colorlog
import yaml
import os
import sys
import time
from _pytest.mark.structures import Mark
import json
#print(sys.argv)
#time.sleep(10)
# @pytest.fixture(scope="function", autouse=True)
# def run_all():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     with open(os.path.join(current_dir, "logging.yaml"), "r") as spec_file:
#         settings = yaml.load(spec_file, Loader=yaml.SafeLoader)
#         logging.config.dictConfig(settings)


def pytest_collection_modifyitems(config, items):
    # asc_list = ["zone", "cluster", "physicalMachine", "main_storage",
    #             "mirrorServer", {"l2network": ["l2net", "vxlan"]}, "l3network",
    #             "calculationSpecifications", "cloudDiskSpec",
    #             "mirror", "cloudDisk", "cloudHost", "recycleBin"]

    asc_list = ["zone", "cluster", "physicalMachine", "main_storage",
                "mirrorServer", "mirror", "calculationSpecifications",
                "cloudDiskSpec","l2net", "vxlan", "l3network_public",
                "l3network_pri", "l3network_system", "cloudRouteImage",
                "cloudRouteSpec", "vpc_router", "vpc_network", "cloudDisk", "cloudHost", "recycleBin"]

    print(sys.argv)
    if {"-m", "delete"} < set(sys.argv):
        asc_list.reverse()
        for item in items[:]:
            if not item.own_markers:
                del items[items.index(item)]
            else:
                flag = 0
                for mark in item.own_markers:
                    if mark.name == "delete":
                        flag = 1
                if not flag:
                    del items[items.index(item)]

    import functools
    def cmp(a, b):
        a_flag_1 = a.name.split("|")[1].split("[")[0]
        b_flag_1 = b.name.split("|")[1].split("[")[0]
        if a_flag_1 in asc_list and b_flag_1 in asc_list:
            if (asc_list.index(a_flag_1) > asc_list.index(b_flag_1)):
                return 1
            elif (asc_list.index(a_flag_1) < asc_list.index(b_flag_1)):
                return -1
            else:
                return 0
        else:
            return 0
    print(len(items))

    items.sort(key=functools.cmp_to_key(cmp))

    for item in items:
         print(item.name)
    # time.sleep(10)
    for item in items:
        #print(item.own_markers)
        for mark in item.own_markers[:]:
            if "dependency" in mark.name:
                if "dependency" == mark.name:
                    item.own_markers.remove(mark)
                    item.add_marker(pytest.mark.dependency())
                else:
                    item.own_markers.remove(mark)
                    mark_attr = mark.name.split(":", 1)
                    depends_val = json.loads(mark_attr[1])
                    item.add_marker(pytest.mark.dependency(depends=depends_val, scope="session"))
        #print(item.own_markers)
        #print(item.name)

    time.sleep(10)



    """
    exit_flag_1 = exit_flag_2 = 0
    while 1:
        flag_2 = True
        for item in items:
            if not item.own_markers:
                del items[items.index(item)]
                flag_2 = False
                break
            exit_flag_1 = 1
            flag = 0
            for mark in item.own_markers:
                if mark.name == "delete":
                    flag = 1
            if not flag:
                del items[items.index(item)]
                flag_2 = False
                break
            exit_flag_2 = 1
        if not flag_2:
            continue
        if exit_flag_2 and exit_flag_1:
            break
            
from datetime import datetime
from py._xmlgen import html

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    '''
    修改Description里面的内容，增加中文显示
    '''
    # pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    _description = ""
    report.nodeid = report.nodeid#encode("utf-8").decode("unicode_escape")
    for i in range(len(report.nodeid)):
        if report.nodeid[i] == "[":
            _description = report.nodeid[i+1:-1]
    report._nodeid = _description

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))
    # cells.insert(2, html.th('Test_nodeid'))
    # cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop(2)

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report._nodeid))
    # cells.insert(2, html.td(report.nodeid))
    # cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))
    cells.pop(2)
"""