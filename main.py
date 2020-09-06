import requests
import os

schema_http = "http://"
schema_https = "https://"


def print_hello():
    print("Welcome to IsItDown.py!")
    print("Please write a URL or URLs you want to check. (separated by comma)")


def check_url_type(url_str):
    urls = url_str.lower()

    if urls.__contains__(","):
        urls_list = urls.replace(" ", "").split(",")
        return urls_list
    else:
        return urls


def check_param(url_param):
    if type(url_param) is str:
        if url_param.startswith(schema_http) or url_param.startswith(schema_https):
            check_connect(url_param)
        else:
            if url_param.__contains__("."):
                check_connect(schema_http + url_param)
            else:
                print(f"{url_param} is a valid URL.")
    elif type(url_param) is list:
        for url in url_param:
            if url.startswith(schema_http) or url.startswith(schema_https):
                check_connect(url)
            else:
                check_connect(schema_http + url)


def check_connect(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            print(f"{url} is up!")
    except:
        print(f"{url} is down!")


print_hello()
check_param(check_url_type(input().lower().replace(" ", "").replace("\t", "")))
while True:
    print("Do you want to start over? y/n ", end='')
    param = input().lower()
    if param == 'y':
        os.system("clear")
        print_hello()
        check_param(check_url_type(input().lower().replace(" ", "").replace("\t", "")))
    elif param == 'n':
        print("ok. bye")
        break
    else:
        print("That's not a valid answer")
        pass
