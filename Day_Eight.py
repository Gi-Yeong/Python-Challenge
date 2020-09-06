import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("cls")
alba_url = "http://www.alba.co.kr"
super_brand_list = []


def save_csv(brand_name, brand_info):
    file = open(f"{brand_name}.csv", "w", encoding="utf-8", newline="")
    writer = csv.writer(file)
    writer.writerow(["place", "title", "time", "pay", "date"])
    if brand_info:
        for brand in brand_info:
            writer.writerow([
                brand["place"],
                brand["title"],
                brand["time"],
                brand["pay"],
                brand["date"]
            ])
    else:
        writer.writerow(["There is No Info"])
    file.close()


def get_super_brand():
    alba_request = requests.get(alba_url)
    alba_result = BeautifulSoup(alba_request.text, "html.parser")
    super_brand = alba_result.find("div", {"id": "MainSuperBrand"}).find("ul", {"class": "goodsBox"}).find_all("li")
    for brand in super_brand:
        brand_name = brand.find("span", {"class": "company"}).text
        brand_url = brand.find("a", {"class": "goodsBox-info"})["href"]
        brand_dict = {"name": brand_name, "url": brand_url}
        super_brand_list.append(brand_dict)


def make_detail_list():
    for brand in super_brand_list:
        res = requests.get(brand["url"])
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.find("tbody").find_all("tr")
        make_list(rows, brand)


def make_list(rows, brand):
    normal_brand_list = []
    for row in rows:
        if row.find("td", {"class": "local first"}):
            place = row.find("td", {"class": "local first"}).text.replace("\xa0", " ")
            title = row.find("span", {"class": "company"}).text.strip()
            time = row.find("td", {"class": "data"}).text
            pay = row.find("td", {"class": "pay"}).text
            date = row.find("td", {"class": "regDate last"}).text
            brand_dict = {
                "place": place,
                "title": title,
                "time" : time,
                "pay"  : pay,
                "date" : date
            }
            normal_brand_list.append(brand_dict)
    save_csv(brand["name"], normal_brand_list)


get_super_brand()
make_detail_list()
