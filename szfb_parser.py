# import csv
# import datetime

from hockey_slovakia_parser import membership
from hockey_slovakia_parser import get_age
from hockey_slovakia_parser import print_matches_list
from hockey_slovakia_parser import save


import urllib.request
from bs4 import BeautifulSoup

from pathlib import Path


def parser():
    URL = 'http://statistiky.szfb.sk/aktualne/vsetky-regiony'
    matches = []

    html = urllib.request.urlopen(URL).read()
    doc = BeautifulSoup(html, features='html.parser')

    table = doc.find(
        'table', {'class': 'table table-condensed table-hover table-striped'}).tbody

    rows_list = table.findAll('tr')

    for row in rows_list:
        columns = row.findAll('td')
        if(membership(columns[-3].text.strip())
           and
           'príp' not in columns[0].text.strip()
           and
           'žia' not in columns[0].text.strip()
           ):
            matches.append({
                'sportname': "Флорбол",
                'tournament': columns[0].text.strip().split('\n')[0],
                'home': columns[2].text.strip().split('\n')[0],
                'guest': columns[2].text.strip().split('\t')[-1],
                'date': columns[1].text.strip().split('\n')[0],
                'time': columns[1].text.strip().split('\t')[-1],
                'url': URL,
                'age': get_age(columns[0].text.strip().split('\n')[0]),
                'place': ""
            })
    return matches


def main():
    matches = parser()
    for counter, match in enumerate(matches, 1):
        print(counter, match, sep=" ")

    save(matches, Path().absolute() / r"csv\florball.csv")


if __name__ == '__main__':
    main()
