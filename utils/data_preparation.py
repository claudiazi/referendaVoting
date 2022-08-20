from ast import literal_eval
import time
import pandas as pd
from pymongo import MongoClient

from config import (
    referendum_columns,
    votes_columns,
    referendum_columns_convert_to_int,
    votes_columns_convert_to_float,
)


def load_data(mongodb_url: str, db_name: str, table_name: str) -> pd.DataFrame:
    start_time = time.time()
    client = MongoClient(mongodb_url)
    db = client[db_name]
    table = db[table_name]
    print(client.server_info())
    df = pd.DataFrame(list(table.find()))
    print(f"{table_name} has been loaded {(time.time() - start_time):.2f}s")
    return df

    cursor = trade_collection.find({"dt": {"$gte": start_dt, "$lt": end_dt}}).sort("dt")
    cursor.batch_size(50000)
    elems = []
    for c in cursor:
        elems.append(c)
    df_trades = pd.DataFrame(elems)

    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))


def extract_status_time(df: pd.DataFrame, status: str) -> pd.DataFrame:
    df = df[df.status == "started"]
    df[f"{status}_at"] = df["timeline"].apply(lambda x: x.get("time"))
    df = df.drop(["timeline", "status"], axis=1)
    return df


def preprocessing_referendum(df: pd.DataFrame) -> pd.DataFrame:
    referendum_df = df[referendum_columns]
    referendum_df["has_passed"] = referendum_df["status"].apply(
        lambda x: "t"
        if x in ["executed", "Passed"]
        else ("wip" if x == "started" else "f")
    )
    referendum_df = referendum_df.rename(
        columns={
            "pre_image_author_address": "author_address",
            "pre_image_call_module": "call_module",
            "pre_image_call_name": "call_name",
        }
    )

    for col in referendum_columns_convert_to_int:
        referendum_df[col] = referendum_df[col].apply(lambda x: int(x) if x is not None and x != 'NULL' else None)
    referendum_df["turnout_perc"] = (
        referendum_df["turnout"] / referendum_df["total_issuance"]
    )
    referendum_df["avg_aye_conviction_rate"] = (
        referendum_df["aye_without_conviction"] / referendum_df["aye_amount"]
    )
    referendum_df["avg_nay_conviction_rate"] = (
        referendum_df["nay_without_conviction"] / referendum_df["nay_amount"]
    )
    return referendum_df


def preprocessing_votes(df: pd.DataFrame) -> pd.DataFrame:
    votes_df = df[votes_columns]
    idx = (
        votes_df.groupby(["referendum_index", "account_address"])[
            "voting_time"
        ].transform(max)
        == votes_df["voting_time"]
    )
    votes_df = votes_df[idx]
    for col in votes_columns_convert_to_float:
        votes_df[col] = votes_df[col].astype("float")
    votes_df["voted_amount_without_conviction"] = votes_df["amount"].apply(
        lambda x: x / 1000000000000
    )
    votes_df["voted_amount_with_conviction"] = round(
        votes_df["voted_amount_without_conviction"] * votes_df["conviction"], 4
    )
    votes_df["voting_time"] = pd.to_datetime(
        votes_df["voting_time"], unit="s"
    ).dt.strftime("%Y-%m-%d")
    votes_df = votes_df[votes_columns]
    return votes_df


if __name__ == "__main__":
    import os

    mongodb_url = os.getenv("MONGODB_URL")
    db_name = os.getenv("DB_NAME")
    table_name = "vote"
    # table_name = os.getenv("TABLE_NAME")
    df = load_data(mongodb_url=mongodb_url, db_name=db_name, table_name=table_name)
    df = pd.read_csv('referendum_data.csv')
    votes_df = preprocessing_votes(df)
    referendum_df = preprocessing_referendum(df)
    print(1)
