import csv
import random
import requests
import json
import os
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

user_agent = UserAgent().random
headers = {
    'Accept': '*/*',
    'User-Agent': user_agent
}
base_url = 'http://health-diet.ru'
url = 'http://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

response = requests.get(url, headers=headers)
src = response.text

soup = BeautifulSoup(src, 'lxml')
all_products_href = soup.find_all(class_='mzr-tc-group-item-href')

all_categories = {
    item.text: base_url + item.get('href')
    for item in all_products_href
}

iteration_count = len(all_categories)
count = 0
print(f'Всего итераций: {iteration_count}')


def replace_characters(category_name):
    replacements = [',', ' ', '-', "'"]
    for item in replacements:
        if item in category_name:
            category_name = category_name.replace(item, '_')
    return category_name


def save_html(category_name, src):
    with open(f'data/{count}_{category_name}.html', 'w') as file:
        file.write(src)


def save_csv(category_name, table_head):
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((product, calories, proteins, fats, carbohydrates))


def save_json(category_name, products_info):
    with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
        json.dump(products_info, file, indent=4, ensure_ascii=False)


def process_category(category_name, category_href):
    category_name = replace_characters(category_name)
    response = requests.get(url=category_href, headers=headers)
    src = response.text
    save_html(category_name, src)

    with open(f'data/{count}_{category_name}.html') as file:
        src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        alert_block = soup.find(
            class_='uk-alert uk-alert-danger uk-h1 uk-text-center mzr-block mzr-grid-3-column-margin-top')
        if alert_block is not None:
            return

        table_head = soup.find('table',
                               class_='uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed').find(
            'tr').find_all('th')

        save_csv(category_name, table_head)

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
                writer.writerow((title, calories, proteins, fats, carbohydrates))

        save_json(category_name, products_info)


def main():
    global count
    global iteration_count
    for category_name, category_href in all_categories.items():
        process_category(category_name, category_href)
        count += 1
        iteration_count -= 1
        print(f'Итерация {count}. {category_name} завершена.')
        print(f'Осталось {iteration_count} итераций')
        time.sleep(random.randrange(2, 4))

    print('Работа завершена')


if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    main()
