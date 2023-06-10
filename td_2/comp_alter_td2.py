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

# Отправляем GET-запрос на страницу
response = requests.get(url, headers=headers)
src = response.text

soup = BeautifulSoup(src, 'lxml')

# Получаем ссылки на все категории продуктов
all_products_href = soup.find_all(class_='mzr-tc-group-item-href')

# Создаем словарь, где ключом является название категории, а значением - ссылка на категорию
all_categories = {
    item.text: base_url + item.get('href')
    for item in all_products_href
}

iteration_count = len(all_categories)
count = 0
print(f'Всего итераций: {iteration_count}')


def replace_characters(category_name):
    """Заменяет определенные символы в названии категории"""
    replacements = [',', ' ', '-', "'"]
    for item in replacements:
        if item in category_name:
            category_name = category_name.replace(item, '_')
    return category_name


def save_combined(category_name, table_head, products_info):
    """Сохраняет данные в одном файле CSV и отдельных файлах JSON и HTML"""
    filename = f'data/{count}_{category_name}.csv'

    with open(filename, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(('Product', 'Calories', 'Proteins', 'Fats', 'Carbohydrates'))

        for item in products_info:
            writer.writerow((item['Title'], item['Calories'], item['Proteins'], item['Fats'], item['Carbohydrates']))

    with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
        json.dump(products_info, file, indent=4, ensure_ascii=False)

    with open(f'data/{count}_{category_name}.html', 'w') as file:
        file.write(src)


def process_category(category_name, category_href):
    """Обрабатывает каждую категорию продуктов"""
    category_name = replace_characters(category_name)

    # Отправляем GET-запрос на страницу категории
    response = requests.get(url=category_href, headers=headers)
    src = response.text

    save_combined(category_name, table_head, products_info)

    print(f'Итерация {count}. {category_name} завершена.')
    print(f'Осталось {iteration_count} итераций')
    time.sleep(random.randrange(2, 4))


def main():
    """Основная функция, выполняющая скрапинг данных"""
    for category_name, category_href in all_categories.items():
        process_category(category_name, category_href)
        count += 1
        iteration_count -= 1

    print('Работа завершена')


if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    main()
