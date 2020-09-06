import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("cls")

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""


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
        items = str(item).replace("<td>", "").replace("</td>", "").replace("[", "").replace(" ", "").split(",")
        if items[1].__contains__("No universal currency") is False:
            country_data = {
                'country' : items[0],
                'currency': items[2]
            }
        country_currency_data.append(country_data)
    return country_currency_data


def print_dict(list):
    for i, dict_item in enumerate(list):
        print("#", i + 1, dict_item['country'])


def find_currency(find_index_list):
    first_item = country_currency_data[find_index_list[0] - 1]
    second_item = country_currency_data[find_index_list[1] - 1]
    first_code = first_item['currency']
    second_code = second_item['currency']
    print(f"How many {first_code} do you want to convert to {second_code}")
    while True:
        try:
            convert = int(input())
            convert_currency(convert, first_code, second_code)
            break
        except ValueError:
            print("That wasn't a number. 1")


def convert_currency(convert, first_code, second_code):
    url = f"https://transferwise.com/gb/currency-converter/{first_code}-to-{second_code}-rate?amount={convert}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    convert_data = soup.find("span", {"class": "text-success"}).text
    result = format_currency(float(convert_data) * convert, second_code, locale="ko_KR")
    amount = format_currency(convert, first_code, locale="ko_KR")
    print(f"{amount} is {result}")


def main():
    print("Hello! Please choose select a country by number: ")
    find_index_list = []
    while True:
        print("#: ", end="")
        try:
            index = int(input())
            length = len(country_currency_data)
            if 1 <= index <= length:
                find_index_list.append(index)
                print(country_currency_data[index - 1]['country'])
                if len(find_index_list) == 2:
                    find_currency(find_index_list)
                    break
                else:
                    print("Now choose another country.")
            else:
                print("Choose a number from the list")
        except ValueError:
            print("That wasn't a number")


data_list = get_data()
make_table_data(data_list)
print_dict(country_currency_data)
main()
