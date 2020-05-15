from box import Box

def check_login_response_headers(response):
    print(response.headers)
    print(2222222222)
    result = False
    if "cloud0" in response.headers.get("Set-Cookie"):
        result = True
    assert result == True


def check_stop_py_machine(response):
    print(response.json())
    assert response.json().get("code") == 0