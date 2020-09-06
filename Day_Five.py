import os
import requests
from bs4 import BeautifulSoup

os.system("cls")
url = "https://www.iban.com/currency-codes"

country_currency_data = []


def get_data():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table_data = soup.find('tbody').find_all('tr')

    result_list = []
    for data in table_data:
        result_list.append(data.findAll('td'))
    return result_list


def make_table_data(list_param):
    for item in list_param:
        items = str(item).replace("<td>", "").replace("</td>", "").replace("[", "").split(",")
        if items[1].__contains__("No universal currency") is False:
            country_data = {
                'country' : items[0],
                'currency': items[2]
            }
        country_currency_data.append(country_data)
    return country_currency_data


def print_dict(list):
    for i, dict_item in enumerate(list):
        print("#", i, dict_item['country'])


def find_currency(index):
    item = country_currency_data[index - 1]
    country = item['country']
    code = item['currency']
    print(f"You chose {country}")
    print(f"The currency code is {code}")


def main():
    print("Hello! Please choose select a country by number: ")
    while True:
        print("#: ", end="")
        try:
            index = int(input())
            length = len(country_currency_data)
            if 1 <= index <= length:
                find_currency(index)
                break
            else:
                print("Choose a number from the list")
        except:
            print("That wasn't a number")


data_list = get_data()
make_table_data(data_list)
print_dict(country_currency_data)
main()
