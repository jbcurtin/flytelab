"""
Hello World
------------
This simple workflow calls a task that returns "Hello World" and then just sets that as the final output of the workflow.
"""
from datetime import datetime
import time
import typing
from typing import Dict, List, Tuple

import pandas as pd
from flytekit import task, workflow

from tasks import preprocess

DELAY = 10


@task
def parse_json_reviews(*, reviews: str) -> Tuple[dict, List[str]]:
    reviews, user_ids = preprocess.parse_json_reviews(reviews = reviews)
    return reviews, user_ids

@task
def find_emoji_url(*, user_ids: List[str]) -> Tuple[dict, List[str]]:
    user_urls = preprocess.find_emoji_url(user_ids = user_ids)
    return user_urls

@task
def parse_emoji_counts(*, user_urls: List[str]) -> str:
    time.sleep(DELAY)
    # emoji_counts: Dict[str, int], e.g.,
    # {id: 21345098234502345, emoji: {"take_my_steam_shit": 1234", ...}}
    emoji_counts = preprocess.parse_emoji_counts(user_urls = user_urls)
    return emoji_counts

@task
def aggregate_reviews(*, reviews: List[dict], emojis_counts: dict) -> pd.Dataframe:
    df = aggregate_review_emoji(reviews = reviews, emoji_counts = emojis_counts)
    return df

@workflow
def data_ingestion(*, reviews: str) -> pd.Dataframe:
    reviews, user_ids = parse_json_reviews(reviews = reviews)
    user_urls = find_emoji_url(user_ids = user_ids)
    emoji_counts = parse_emoji_counts(user_urls = user_urls)
    df = aggregate_reviews(reviews = reviews, emoji_counts = emoji_counts)
    return df


if __name__ == "__main__":
    print('Running Workflow')
    print(f"Results: { data_ingestion(reviews = "json-reviews.json") }")
