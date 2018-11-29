from pathlib import Path

from hockey_slovakia_parser import parser as hc_parse
from hockey_slovakia_parser import save
from szfb_parser import parser as flb_parse


def main():
    matches = []
    matches.extend(flb_parse())
    matches.extend(hc_parse())

    matches.sort(key=lambda match: (match['date'], match['time']))
    save(matches, Path().absolute() / r"csv\matches.csv")
    print('[SUMMARY] Total result: %d' % len(matches))


if __name__ == "__main__":
    main()
