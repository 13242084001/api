#!/usr/bin/python3.6
#
from box import Box

def test_function(response):
    print(response)
    return Box({"test_user_name": response.json()["user"]["name"]})

def save_cookie(response):
    print(response.headers)
    print(response.content)
    cookies = response.headers.get("Set-Cookie").split()
    des_cookie = "my_id=administrator; LOCALE=zh_CN;"
    for co in cookies:
        print(co)
        if "JSESSIONID" in co or "cloud" in co:
            tmp_str = " " + co
            des_cookie += tmp_str
    print(des_cookie)
    return Box({"cookie": des_cookie})
