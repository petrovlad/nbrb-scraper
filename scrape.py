import logging
from datetime import date, timedelta
from typing import List

import requests
from bs4 import BeautifulSoup
from requests import Response

from database import MySQLDB

# CONSTS
SCRAPE_SIZE = 30  # days before
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
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


def daterange(start_date: date, end_date: date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def execute_target_request(target_date: date) -> Response:
    raw_data = f'Date={target_date.year}-{target_date.month}-{target_date.day}&Type=Day&X-Requested-With=XMLHttpRequest'
    resp = requests.get(BASE_URL, headers=BASE_HEADERS, data=raw_data)
    log.debug(f'{resp.status_code=}, {resp.text=}')
    return resp


def parse_course_info(soup: BeautifulSoup) -> (str, str, float, float):
    cur_name = soup.find('td', class_='curName').find('div').find('span').text
    cur_abrv_amount = soup.find('td', class_='curAmount').text.replace(',', '.').split(' ')
    cur_amount = float(cur_abrv_amount[0])
    cur_abrv = cur_abrv_amount[1]
    cur_course = float(soup.find('td', class_='curCours').find('div').text.replace(',', '.'))
    return cur_name, cur_abrv, cur_amount, cur_course


def parse_course_infos(text: str) -> List[dict]:
    ret = list()
    currencies_soup = (BeautifulSoup(text, 'html.parser')
                       .find('tbody')
                       .findChildren('tr'))
    for currency_soup in currencies_soup:
        cur_name, cur_abrv, cur_amount, cur_course = parse_course_info(currency_soup)
        ret.append({
            'currency_name': cur_name,
            'currency_abbreviation': cur_abrv,
            'currency_amount': cur_amount,
            'currency_course': cur_course
        })
    return ret


def main():
    database = MySQLDB('localhost', 'aboba', 'aboba', 'nbrb_scraper')
    database.clear_stats()

    end_date = date.today()
    start_date = end_date - timedelta(days=SCRAPE_SIZE)
    for _date in daterange(start_date, end_date):
        resp = execute_target_request(_date)
        course_list = parse_course_infos(resp.text)
        for course in course_list:
            cur_name = course['currency_name']
            cur_abrv = course['currency_abbreviation']
            cur_amount = course['currency_amount']
            cur_course = course['currency_course']
            log.debug(f'{_date}-{cur_name}-{cur_amount}-{cur_course}')
            database.add_course_stat(
                _date,
                cur_name,
                cur_abrv,
                cur_amount,
                cur_course,
            )
        log.info(f'Fetched date {_date}')


if __name__ == '__main__':
    main()
