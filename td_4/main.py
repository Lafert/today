import json

import lxml
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

base_url = 'https://www.skiddle.com'
user_agent = UserAgent().random
headers = {
    'User-Agent': user_agent
}
count = 24


def get_url():
    global count
    for i in range(3):
        url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=11%20Jun%202023&to_date=&genre%5B%5D=pop&maxprice=500&o={count}&bannertitle=July'
        count += 24
        # print(url)
        yield url


def get_card_url():
    url_generator = get_url()
    fests_url_list = []
    for url in url_generator:
        response = requests.get(url, headers=headers)
        if 'No festivals found.' in response:
            print("No festivals found. Exiting...")
            break

        json_data = json.loads(response.text)
        html_response = json_data['html']

        # with open(f'index_{count-24}.html', 'w') as file:
        #     file.write(html_response)
        # with open(f'index_{count - 24}.html') as file:
        #     src = file.read()

        soup = BeautifulSoup(html_response, 'lxml')
        cards = soup.find_all('a', class_='card-details-link')
        for card in cards:
            card_href = base_url + card.get('href')
            fests_url_list.append(card_href)
    return fests_url_list

def get_data():
    for item in get_card_url():
        response = requests.get(item, headers=headers).text

        try:
            soup_data = BeautifulSoup(response, 'lxml')
            fest_info_block = soup_data.find(class_='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-1ik2gjq')
            fest_name = soup_data.find('h1', class_='MuiTypography-root MuiTypography-body1 css-r2lffm').text.strip()
            fest_data_list = fest_info_block.find(class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol').find_all('span')
            fest_date = fest_data_list[0].text + fest_data_list[1].text
            print(fest_name, fest_date)



        except Exception as ex:
            print(ex)
            print('Damn....There was some error...')

get_data()


