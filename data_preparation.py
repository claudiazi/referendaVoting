import datetime

import pandas as pd
from pymongo import MongoClient


def load_data(mongodb_url: str, db_name: str, table_name: str) -> pd.DataFrame:
    client = MongoClient(mongodb_url)
    db = client[db_name]
    table = db[table_name]
    df = pd.DataFrame(list(table.find()))
    return df


def preprocessing(df: pd.DataFrame):
    df = df.explode("votes")
    df = pd.concat([df, df.votes.apply(pd.Series)], axis=1)
    df["balance"] = pd.to_numeric(df["balance"]).apply(lambda x: x / 1000000000)
    df["time"] = df["time"].apply(
        lambda x: datetime.datetime.fromtimestamp(x / 1000).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )
    return df
