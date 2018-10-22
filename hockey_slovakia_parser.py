import argparse

import csv
import datetime
import urllib.request

from bs4 import BeautifulSoup

DOMAIN = "https://www.hockeyslovakia.sk"
BASE_URL = "https://www.hockeyslovakia.sk/sk/stats/live-matches/"

path_to_save = r"D:\Google Drive\pythonCrawler\sport_matches.csv"


def main():
    matches_list = []

    # For local tests:

    # matches_list.extend(parse(open(r"D:\test.html", "r", encoding="utf-8").read()))
    # print_matches_list(matches_list)

    # Being online:
    next_day = datetime.datetime.now()
    # We're looking for matches taking place the next -n- month
    while next_day.month <= datetime.datetime.now().month + 1:
        # https://www.hockeyslovakia.sk/sk/stats/live-matches?Day=16.08.2018
        matches_list.extend(
            parse(get_html(BASE_URL + "?Day=" + next_day.strftime("%d.%m.%Y"))))
        print("Parsing of day {} has been completed.".format(
            next_day.strftime("%d.%m.%Y")))
        next_day = next_day + datetime.timedelta(days=1)
        # break

    # print_matches_list(
    #     list(filter(lambda match: "KOŠICE" in match['place'].upper() or "MICHALOVCE" in match[
    #         'place'].upper() or "SPÍŠSKÁ NOVÁ VES" in match['place'].upper() or "PREŠOV" in match[
    #                                   'place'].upper() or "VRANOV" in match['place'].upper(),
    #                 matches_list)))

    matches_list = list(filter((lambda match: match["age"] not in ["U14", "U16"] and membership(
        match["place"]) and "tipsport" not in match["tournament"].lower()), matches_list))
    # matches_list = list(filter(lambda match: membership(match["place"]), matches_list))
    print_matches_list(matches_list)

    # Make sense from out of this whole thing..
    save(matches_list, path_to_save)


# TODO: ENSURE THE FORMAT OF SAVING INTO CSV TO EASILY COPY-PASTE INTO THE MAIN SPREAD SHEET
def save(matches_list, path):
    for match in matches_list:
        match['time'] = datetime.datetime.strptime(
            match['time'], "%H:%M") + datetime.timedelta(hours=1)
        match['time'] = match['time'].strftime("%H:%M")

    with open(path, 'w', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        writer.writerow(('Date', 'Time', 'Hockey', 'Tournament',
                         'Home', 'Age', "", 'Guests', 'Age', 'Place', 'URL'))
        for match in matches_list:
            writer.writerow((match['date'], match['time'], "Хоккей",
                             match['tournament'],
                             match['home'], match['age'], "vs",
                             match['guest'], match['age'],
                             " ".join(("at", match['place'])), match['url']))


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def print_matches_list(matches):
    for index, match in enumerate(matches):
        print(str(index + 1) + '.',
              "tournament: %s" % match['tournament'],
              match['age'],
              match['home'], "VS", match['guest'],
              match['date'], "at", match['time'], "in",
              match['place'], "match_url: %s" % match['url'])


def get_age(tournament):
    tournament = tournament.upper()
    if "KADET" in tournament:
        return "U16"
    elif "DORAST" in tournament:
        return "U18"
    elif "JUNIOR" in tournament:
        return "U20"
    elif "ŽIAK" in tournament:
        return "U14"
    else:
        return "Взрослые"


def parse(html):
    # the entire page
    soup = BeautifulSoup(html, features="html.parser")
    # soup.find_parent('div', class_='panel-body')

    # find all the rows of sport matches
    rows = soup.findAll('tr', class_='fn-tap-row')
    matches = []

    # add every match placed in row
    for row in rows:
        cols = row.findAll('td')
        matches.append({
            'tournament': row.find_parent('div', class_='panel-body').div.text.strip(),
            'home': cols[0].div.text.strip(),
            'guest': cols[2].div.text.strip(),
            'date': cols[3].findChildren()[2].text.strip(),
            'time': cols[3].findChildren()[3].text.strip(),
            'place': cols[3].findChildren()[4].text.strip(),
            'url': DOMAIN + cols[3].findChildren()[5].a['href'],
            'age': get_age(row.find_parent('div', class_='panel-body').div.text.strip())
        })
        # break

    return matches


def membership(place):
    import unidecode

    my_cities = ["kosic", "michalovc", "presov", "spisk", "vranov"]

    for city in my_cities:
        if city in unidecode.unidecode(place).lower():
            return True

    return False


def test():
    time = "14:00"
    hour = datetime.timedelta(hours=1)
    time_obj = datetime.datetime.strptime(time, "%H:%M") + hour

    print(time_obj.strftime("%H:%M"))


if __name__ == '__main__':
    main()
    # test()
    # TODO: Implement support of arguments, such as PATH, DAYS_AHEAD, CITIES, AGE CATEGORIES
    # parser = argparse.ArgumentParser()
    # parser.add_argument("path", help="absolute path to output csv")
    # args = parser.parse_args()
    # print(args.path)
