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
    df["totalIssuance"] = df["totalIssuance"].astype(str).astype(float)
    df["balance"] = df["balance"].astype(str).astype(float)
    df["id"] = df["id"].astype(int)
    # df["balance"] = pd.to_numeric(df["balance"]).apply(lambda x: x / 1000000000)
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df = df.drop("votes", axis=1)
    return df
