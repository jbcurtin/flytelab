import json
import os
import random
import re
import sys
import time
from typing import List

import requests
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], ".."))


def load_steamids_from_raw(*, jsonfile: str) -> List[str]:
    with open(jsonfile, "r") as json_file:
        data = json.load(json_file)

    steam_ids = [review["author"]["steamid"] for review in data]
    return steam_ids


def get_personaname_from_id(*, steamids: List[str], checkpoint: int = 50) -> List[str]:
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

    for idx, steamid in enumerate(tqdm(steamids[8250:])):
        url = prefix + steamid
        response = requests.get(url, headers=headers)
        name = re.findall(key, response.text)
        if name:
            steamid_personaname_mapping[steamid] = name[0]

        if idx % checkpoint == 0:
            with open(out_file, "w", encoding="utf-8") as jsonfile:
                json.dump(steamid_personaname_mapping, jsonfile)

        time.sleep(random.uniform(0, 0.3))

    return steamid_personaname_mapping


def main():
    RAW_REVIEW_FILE = "dataset/raw/json-reviews.json"
    steam_ids = load_steamids_from_raw(jsonfile=RAW_REVIEW_FILE)
    personanames = get_personaname_from_id(steamids=steam_ids)
    print(personanames[-1])


if __name__ == "__main__":
    main()
