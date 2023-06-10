import csv
import random

import requests
from bs4 import BeautifulSoup
import lxml
from fake_useragent import UserAgent
import json
from time import sleep

user_agent = UserAgent().random
headers = {
    'Accept': '*/*',
    'User-Agent': user_agent
}
base_url = 'http://health-diet.ru'
url = 'http://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

response = requests.get(url, headers=headers)
src = response.text
# print(src)

with open('index.html', 'w') as file:
    file.write(src)

with open('index.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
all_categories_dict = {}
all_products_href = soup.findAll(class_='mzr-tc-group-item-href')
for item in all_products_href:
    item_text = item.text
    item_href = base_url + item.get('href')
    all_categories_dict[item_text] = item_href

with open('all_categories_dict.json', 'w') as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open('all_categories_dict.json') as file:
    all_categories = json.load(file)

# print(all_categories)
iteretion_count = int(len(all_categories)) - 1
count = 0
print(f'Всего  итераций {iteretion_count}')

for category_name, category_href in all_categories.items():

    rep = [',', ' ', '-', "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')
    # print(category_name)

    response = requests.get(url=category_href, headers=headers)
    src = response.text

    with open(f'data/{count}_{category_name}.html', 'w') as file:
        file.write(src)

    with open(f'data/{count}_{category_name}.html') as file:
        src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        alert_block = soup.find(
            class_='uk-alert uk-alert-danger uk-h1 uk-text-center mzr-block mzr-grid-3-column-margin-top')
        if alert_block is not None:
            continue

        table_head = soup.find('table',
                               class_='uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed').find(
            'tr').find_all('th')
        # print(table_head)
        product = table_head[0].text
        calories = table_head[1].text
        proteins = table_head[2].text
        fats = table_head[3].text
        carbohydrates = table_head[4].text

        with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    product,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

    products_data = soup.find(
        class_='uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed').find(
        'tbody').find_all('tr')

    products_info = []

    for item in products_data:
        products_tds = item.find_all('td')
        title = products_tds[0].find('a').text
        calories = products_tds[1].text
        proteins = products_tds[2].text
        fats = products_tds[3].text
        carbohydrates = products_tds[4].text

        products_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }
        )

        with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
    with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
        json.dump(products_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f'Итерация {count}. {category_name} за    писан.')
    iteretion_count = iteretion_count - 1

    if iteretion_count == 0:
        print('Работа закончена')
        break

    print(f'Осталость {iteretion_count} итераций')
    sleep(random.randrange(2, 4))
