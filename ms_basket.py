import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup as bs

from hockey_slovakia_parser import (get_age, membership, print_matches_list,
                                    save)

URL = "http://msbasket.sk/program/zapasyOblast?q=program/zapasy"


def parser():
    # print('here it comes!')
    matches = []
    html = urllib.request.urlopen(URL).read()
    doc = bs(html, features="html.parser")

    list_of_tables = doc.findAll(
        'table', {'class': 'basketTablePrehladZapasov'})

    for table in list_of_tables:

        # date = table.get('id').split('|')[0]

        rows = table.findAll('tr', {'class': 'trBasketTableDataParne'})
        rows.extend(table.findAll('tr', {'class': 'trBasketTableDataNeparne'}))

        for row in rows:
            cols = row.findAll('td')
            # time's not present -> go ahead
            if len(cols[0].text) == 0:
                continue
            tournament = cols[1].text.strip()
            city = cols[5].text.strip()
            if(membership(city)
               and
               'kadet' not in tournament
               and
               'žia' not in tournament
               and
               'U16' not in get_age(tournament) ):

                matches.append({
                    'sportname': "Баскетбол",
                    'tournament': tournament,
                    'home': cols[2].text.strip(),
                    'guest': cols[3].text.strip(),
                    'date': table.get('id').split('|')[0],
                    'time': cols[0].text.strip(),
                    'place': " ".join([city, "[%s]" % cols[4].text.strip()]),
                    'url': URL,
                    'age': get_age(tournament)
                })
    print('[BASKETBALL] Parsing and collecting completed! Result: %d' %
          len(matches))
    return matches
    # for index, match in enumerate(matches, 1):
    #     print(index, match, sep=' ')


if __name__ == "__main__":
    matches = parser()
    for counter, match in enumerate(matches, 1):
        print(counter, match, sep=" ")

    save(matches, Path().absolute() / r"csv\basketball.csv")
