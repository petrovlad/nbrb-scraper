from database import MySQLDB
from matplotlib import pyplot as plt
from itertools import groupby


def main():
    db = MySQLDB('localhost', 'aboba', 'aboba', 'nbrb_scraper')
    data = db.get_all()
    grouper_func = lambda _stat: _stat['currency_name']
    for key, stats_by_key in (groupby(sorted(data, key=grouper_func), key=grouper_func)):
        stats = list(stats_by_key)
        x = [s['date'] for s in stats]
        y = [s['currency_course'] for s in stats]
        plt.plot(x, y, label=f"{stats[0]['currency_name']} ({stats[0]['currency_amount']})")
    plt.legend(loc='lower left')
    plt.show()


if __name__ == '__main__':
    main()
