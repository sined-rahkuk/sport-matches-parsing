from hockey_slovakia_parser import parser as hc_parse
from szfb_parser import parser as flb_parse

from hockey_slovakia_parser import save
from pathlib import Path


def main():
    matches = []
    matches.extend(hc_parse())
    matches.extend(flb_parse())

    matches.sort(key=lambda match: (match['date'], match['time']))
    save(matches, Path().absolute() / r"csv\matches.csv")


if __name__ == "__main__":
    main()
