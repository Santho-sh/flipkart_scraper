import requests
import json
from bs4 import BeautifulSoup
from colorama import Fore, Style
import re
import math


def main():

    with open("search.json", "r") as file:
        mobiles = json.load(file)

    output_arr = []
    not_found = []

    for mobile in mobiles:
        try:
            print(Fore.GREEN + "currently scrapping: " + mobile + Style.RESET_ALL)
            result = get_re(mobile)

            if result != None:
                output_arr.append(result)
            else:
                print(Fore.RED + "mobile not found: " +
                      mobile + Style.RESET_ALL)
                not_found.append({"mobile": mobile})

        except Exception as e:
            print(Fore.RED + "An exception occurred while scrapping: " +
                  mobile + Style.RESET_ALL)
            print(e)

    with open("output.json", "w") as file:
        json.dump(output_arr, file)
    with open("not_found.json", "w") as file:
        json.dump(not_found, file)


def get_re(mobile):

    url = f"https://www.flipkart.com/search?q={mobile.lower()}&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&marketplace=FLIPKART"

    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html5lib')
    # extract price using class '_16Jk6d'
    all_name = soup.find_all("div", attrs={"class": "_4rR01T"})
    all_price = soup.find_all("div", attrs={"class": "_30jeq3"})
    all_links = soup.find_all("a", attrs={"class": "_1fQZEK"})

    lowest_price = math.inf
    link = ""

    for i in range(len(all_name)):

        if match := re.search(r"(.+) \(.+", all_name[i].text, re.IGNORECASE):

            name = match.group(1).lower()
            if name == mobile.lower():
                price = all_price[i].text
                # remove Rs, commas from price
                price = int(price[1:].replace(",", ""))

                if price < lowest_price:
                    lowest_price = price
                    link = all_links[i]["href"]
                    link = f"https://www.flipkart.com{link}"

                if lowest_price == math.inf or link == "":
                    return None

                link_full = re.search(r"(.+)\?.+", link, re.IGNORECASE)
                link = link_full.group(1)

                result = {"mobile": mobile, "price": lowest_price,
                          "link": link, "search_url": url}

                return result

            else:
                continue


if __name__ == "__main__":
    main()
