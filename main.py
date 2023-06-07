import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import lxml


base_url = ''
user_agent = UserAgent().random
headers = {
    'User-Agent' : user_agent
}