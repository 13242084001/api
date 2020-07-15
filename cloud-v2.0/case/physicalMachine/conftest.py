import pytest
from box import Box

def pytest_collection_modifyitems(config, items):
    items.sort(key=lambda x: x.name)
    #print("after: %s", items)

