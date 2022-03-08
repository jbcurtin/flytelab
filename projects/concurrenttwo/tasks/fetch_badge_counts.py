import json
import os
from random import randint
import re
import sys
import time
from typing import List

import requests
import tqdm

sys.path.append(os.path.join(sys.path[0], ".."))


def load_steamids_from_raw(*, jsonfile: str) -> List[str]:
    with open(jsonfile, "r") as json_file:
        data = json.load(json_file)

    steam_ids = [review["author"]["steamid"] for review in data]
    return steam_ids


def generate_urls(*, steam_ids: List[str]) -> List[str]:
    prefix = "https://steamcommunity.com/profiles/"
    return [prefix + id for id in steam_ids]


def get_username_from_redirect_url(*, urls: List[str]) -> List[str]:
    """YOLO. Not doing async or threading to spam the site. Will have to wait patiently.

    Args:
        urls (List[str]): _description_

    Returns:
        List[str]: _description_
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64;"
            " rv:97.0) Gecko/20100101 Firefox/97.0"
        ),
        "Content-Type": "text/html; charset=UTF-8",
    }
    key = '"personaname":"(.*?)"'
    personanames = []

    for url in tqdm(urls):
        response = requests.get(url, headers=headers)
        # Not sure how many names will the Regex match, so pick only the first entry
        name = print(re.findall(key, response.texte))
        if name:
            personanames.append(name[0])
        time.sleep(randint(0, 2))

    with open("personanames.json", "w", encoding="utf-8") as jsonfile:
        json.dump(personanames, jsonfile)

    return personanames


def main():
    RAW_REVIEW_FILE = "data/raw/json-reviews.json"
    steam_ids = load_steamids_from_raw(jsonfile=RAW_REVIEW_FILE)
    steam_urls = generate_urls(steam_ids=steam_ids)
    personanames = get_username_from_redirect_url(urls=steam_urls)
    print(personanames[-1])


if __name__ == "__main__":
    main()
