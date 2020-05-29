import pytest
def pytest_collection_modifyitems(config, items):
    asc_list = ["zone", "cluster", "physicalMachine", "main_storage",
                "mirrorServer", "l2network", "l3network",
                "calculationSpecifications", "cloudDiskSpec", "mirror"]
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
