import requests
from bs4 import BeautifulSoup

WIKI_PAGE = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%B"  \
            "A_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2"


def parse_countries():
    response = requests.get(WIKI_PAGE)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", class_="wikitable")

    list_of_countries = []
    first_letter_count = {}
    for table in [*tables[:2], *tables[3:]]:
        countries_soup = table.find_all("tr")[1:]

        for country_soup in countries_soup:
            country_name = country_soup.find("a").get("title")
            full_country_name = country_soup.find_all("td")[-1].text.replace("\n", "")
            flag_url = country_soup.find("a").find("img").get("src")
            words_in_full_country_name = len(full_country_name.split(" "))

            list_of_countries.append({
                "country": country_name,
                "full_country_name": full_country_name,
                "words_in_full_country_name": words_in_full_country_name,
                "same_letter_count": 0,
                "flag_url": flag_url,
            })

            first_letter = country_name[0]
            if first_letter in first_letter_count:
                first_letter_count[first_letter] += 1
            else:
                first_letter_count[first_letter] = 1

    for country in list_of_countries:
        country["same_letter_count"] = first_letter_count[country.get("country")[0]]

    return list_of_countries


def print_country_data(country_name: str):
    for country_data in parse_countries():
        if country_data["country"] == country_name:
            print(country_data)
            break


if __name__ == "__main__":
    print_country_data("Украина")
    print_country_data("Финляндия")
    print_country_data("Литва")
