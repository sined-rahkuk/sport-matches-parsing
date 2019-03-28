from datetime import datetime
from pathlib import Path

import dateparser

from hockey_slovakia_parser import parser as hc_parse
from hockey_slovakia_parser import save
from ms_basket import parser as bask_parse
from szfb_parser import parser as flb_parse

import time


def main():
    start = time.time()
    matches = []
    matches.extend(hc_parse())
    matches.extend(bask_parse())
    matches.extend(flb_parse())

    matches.sort(key=lambda match: (match['date'], match['time']))
    save(matches, Path().absolute() / r"csv\matches.csv")

    dates = [dateparser.parse(match['date'],
                              date_formats=['%d.%m.%Y']) for match in matches]

    print('[SUMMARY] Total result: %d matches within a period of %s till %s' %
          (len(matches), min(dates).strftime("%A %d. %B %Y"), max(dates).strftime("%A %d. %B %Y")))

    end = time.time()
    print('Time: %.fs' % (end - start))


if __name__ == "__main__":
    main()
