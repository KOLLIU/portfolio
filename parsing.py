import requests

from bs4 import BeautifulSoup

from sqlalchemy import select, insert, update

from db import CityDB


class City:
    def __init__(self, table_row=None, db_row=None):
        if db_row is None:
            self.number = int(table_row[0].text)
            self.title = table_row[1].text.lower()
            self.title_href = "https://ru.wikipedia.org" + table_row[1].find("a").get("href")
            self.city_district = table_row[2].text
            self.city_district_href = "https://ru.wikipedia.org" + table_row[2].find("a").get("href")
            self.okato = int(table_row[3].text.replace(" ", ""))
            self.population = int(table_row[4].get("data-sort-value"))

            # Вообще здесь должен быть целочисленный тип данных, но первое упоминание Раменского "1760-e"
            self.foundation = table_row[5].text

            self.city_status = int(table_row[6].text)
            self.emblem_href = table_row[7].find("img").get("src")
        else:
            db_row=db_row[0]
            self.number = db_row.number
            self.title = db_row.title
            self.title_href = db_row.title_href
            self.city_district = db_row.city_district
            self.city_district_href = db_row.city_district_href
            self.okato = db_row.okato
            self.population = db_row.population
            self.foundation = db_row.foundation
            self.city_status = db_row.city_status
            self.emblem_href = db_row.emblem_href


    def __str__(self):
        return f'{self.number}) <a href="{self.title_href}">{self.title.capitalize()}</> {self.population}'


class Cities:
    def __init__(self, rows):
        self.cities = [City(row) for row in rows]

    async def update_cities(self, db_session):
        async with db_session() as session:
            for city in self.cities:
                db_city = (await session.execute(select(CityDB).where(CityDB.title == city.title))).fetchone()
                data = {"number": city.number,
                        "title": city.title,
                        "title_href": city.title_href,
                        "city_district": city.city_district,
                        "city_district_href": city.city_district_href,
                        "okato": city.okato,
                        "population": city.population,
                        "foundation": city.foundation,
                        "city_status": city.city_status,
                        "emblem_href": city.emblem_href}
                if db_city is None:
                    await session.execute(insert(CityDB).
                                          values(**data))
                else:
                    await session.execute(update(CityDB).
                                          values(**data).
                                          where(CityDB.title == city.title))
                await session.commit()

    def __str__(self):
        return "\n".join(str(city) for city in self.cities)


def parse_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('table', class_="standard")
    cities = items[0]
    rows = cities.find_all("tr")
    rows = [row.find_all("td") for row in rows[1::]]
    cities = Cities(rows)
    return cities
