coding="utf-8"
import pytest
def pytest_collection_modifyitems(config, items):
    asc_list = ["zone", "cluster", "physicalMachine", "main_storage",
                "mirrorServer", "l2network", "l3network",
                "calculationSpecifications", "cloudDiskSpec", "mirror", "cloudDisk", "cloudHost"]
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

    for item in items:
        #print(type(item))
        print(item.name)
    items.sort(key=functools.cmp_to_key(cmp))
    for item in items:
        print(item.name)

#from datetime import datetime
from py._xmlgen import html
"""
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