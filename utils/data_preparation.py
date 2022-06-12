import datetime
import re
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
    df["voted_ksm"] = pd.to_numeric(df["balance"]).apply(lambda x: x / 1000000000000)
    df["conviction"] = df["conviction"].apply(
        lambda x: 0.1 if x == "None" else int(re.search("\d", x).group())
    )
    df["locked_amount"] = round(df["voted_ksm"] * df["conviction"], 4)
    df["time"] = pd.to_datetime(df["time"], unit="ms").dt.strftime('%Y-%m-%d')
    df = df.drop("votes", axis=1)
    return df


if __name__ == "__main__":
    import os

    mongodb_url = os.getenv("MONGODB_URL")
    db_name = os.getenv("DB_NAME")
    table_name = os.getenv("TABLE_NAME")
    votes_df = load_data(
        mongodb_url=mongodb_url, db_name=db_name, table_name=table_name
    )
    votes_df = preprocessing(votes_df)
    print(1)
