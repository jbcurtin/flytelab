import json
import os
import random
import re
import sys
import time
from typing import Dict, List

import requests
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], ".."))


def load_steamids_from_raw(*, jsonfile: str) -> List[str]:
    with open(jsonfile, "r") as json_file:
        data = json.load(json_file)

    steam_ids = [review["author"]["steamid"] for review in data]
    return steam_ids


def get_personaname_from_id(
    *, steamids: List[str], checkpoint: int = 50
) -> Dict[str, str]:
    """YOLO. Not doing async or threading to spam the site. Use a timer to wait for
    less than 0.5s. Will have to wait patiently.

    Also, not sure how many names will the Regex match, so pick only the first entry.

    Args:
        steamids (List[str]): _description_

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
    prefix = "https://steamcommunity.com/profiles/"
    steamid_personaname_mapping = {}
    out_file = "dataset/raw/steamid_personaname_mapping.json"

    for idx, steamid in enumerate(tqdm(steamids[12492:])):
        url = prefix + steamid
        response = requests.get(url, headers=headers)
        name = re.findall(key, response.text)
        if name:
            steamid_personaname_mapping[steamid] = name[0]

        if idx % checkpoint == 0:
            with open(out_file, "w", encoding="utf-8") as jsonfile:
                json.dump(steamid_personaname_mapping, jsonfile)

        time.sleep(random.uniform(0, 0.3))

    with open(out_file, "w", encoding="utf-8") as jsonfile:
        json.dump(steamid_personaname_mapping, jsonfile)

    return steamid_personaname_mapping


def download_review_pages(*, personaname_file: str):
    """Downloads the review pages for each personaname.

    Args:
        personanames (str): _description_
    """
    with open(personaname_file, "r") as jsonfile:
        personaname_mapping = json.load(jsonfile)

    URL_TEMPLATE = "https://steamcommunity.com/id/{}/recommended/1245620/"
    HTML_FILE_TEMPLATE = "dataset/raw/review_htmls/{}.html"

    for steamid, personaname in tqdm(personaname_mapping.items()):
        url = URL_TEMPLATE.format(personaname)
        response = requests.get(url)
        with open(
            HTML_FILE_TEMPLATE.format(steamid), "w", encoding="utf-8"
        ) as html_file:
            html_file.write(response.text)


def main():
    # RAW_REVIEW_FILE = "dataset/raw/json-reviews.json"
    # steam_ids = load_steamids_from_raw(jsonfile=RAW_REVIEW_FILE)
    # _ = get_personaname_from_id(steamids=steam_ids)

    PERSONA_FILE = "dataset/raw/steamid_personaname_mapping.json"
    download_review_pages(personaname_file=PERSONA_FILE)


if __name__ == "__main__":
    main()
