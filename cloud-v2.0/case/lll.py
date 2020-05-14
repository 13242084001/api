#!/usr/bin/env python3.6
#
import pytest
import requests

data = {"userId": "administrator", "password": "9DyrH0qty0SqrdsvVCjnJQ==", "userType": 0, "loginType": 1}
global_url = "http://172.16.130.252:38080"


def test_login():
	r=requests.post(global_url + "/login.do",verify=False,data=data)
	print(r.headers)
	print(r.content)
	assert r.status_code == 200

test_login()
