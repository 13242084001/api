import pytest

def pytest_collection_modifyitems(config, items):
    for item in items:
        print(item, "kkkkkkk")
        print(type(item))
        print(item.name)
        print(22222222222222222222222)