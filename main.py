import logging
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

from database import MySQLDB

# CONSTS
SCRAPE_SIZE = 60  # days before
BASE_URL = 'https://www.nbrb.by/statistics/rates/ratesdaily.asp'
BASE_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'ASP.NET_SessionId=vl0v4hnmfq0sw0eprqgshnya; _ym_uid=1684478173526043091; _ym_d=1684478173; '
              '_ga=GA1.2.554857727.1684478173; _gid=GA1.2.1850794287.1684478173; _ym_isad=2; _ym_visorc=w',
    'Origin': 'https://www.nbrb.by',
    'Referer': 'https://www.nbrb.by/statistics/rates/ratesdaily.asp',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
}
# LOG CONFIG
log = logging.getLogger('scraper')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


def daterange(start_date: date, end_date: date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def main():
    database = MySQLDB('localhost', 'aboba', 'aboba', 'nbrb_scraper')
    database.clear_stats()

    end_date = date.today()
    start_date = end_date - timedelta(days=SCRAPE_SIZE)
    for _date in daterange(start_date, end_date):
        raw_data = f'Date={_date.year}-{_date.month}-{_date.day}&Type=Day&X-Requested-With=XMLHttpRequest'
        resp = requests.get(BASE_URL, headers=BASE_HEADERS, data=raw_data)
        log.debug(f'{resp.status_code=}, {resp.text=}')
        soup = BeautifulSoup(resp.text, 'html.parser')
        currs_list = soup.find('tbody').findChildren('tr')
        for curr in currs_list:
            cur_name = curr.find('td', class_='curName').find('div').find('span').text
            cur_amount = curr.find('td', class_='curAmount').text.replace(',', '.')
            cur_course = curr.find('td', class_='curCours').find('div').text.replace(',', '.')
            log.debug(f'{_date}-{cur_name}-{cur_amount}-{cur_course}')
            database.add_currency_stat(_date, cur_name, cur_amount, cur_course)


if __name__ == '__main__':
    main()
