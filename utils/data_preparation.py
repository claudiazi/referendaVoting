from ast import literal_eval

import pandas as pd
from pymongo import MongoClient

from config import (
    referendum_columns,
    votes_columns,
    referendum_columns_convert_to_int,
    votes_columns_convert_to_float,
)


def load_data(mongodb_url: str, db_name: str, table_name: str) -> pd.DataFrame:
    client = MongoClient(mongodb_url)
    db = client[db_name]
    table = db[table_name]
    print(client.server_info())
    df = pd.DataFrame(list(table.find()))
    return df


def extract_status_time(df: pd.DataFrame, status: str) -> pd.DataFrame:
    df = df[df.status == "started"]
    df[f"{status}_at"] = df["timeline"].apply(lambda x: x.get("time"))
    df = df.drop(["timeline", "status"], axis=1)
    return df


def preprocessing_referendum(df: pd.DataFrame) -> pd.DataFrame:
    referendum_df = df[referendum_columns]
    referendum_df = referendum_df[
        referendum_df["status"].isin(["executed", "passed", "notPassed"])
    ]
    referendum_df["timeline"] = referendum_df["timeline"].apply(literal_eval)
    referendum_df["pre_image"] = referendum_df["pre_image"].apply(
        lambda x: literal_eval(x) if isinstance(x, str) else None
    )
    timeline_df = referendum_df.explode("timeline")
    timeline_df["status"] = timeline_df["timeline"].apply(lambda x: x.get("status"))
    timeline_df = timeline_df[["referendum_index", "status", "timeline"]]
    for status in ["started", "passed", "notPassed"]:
        extract_df = extract_status_time(timeline_df, status)
        referendum_df = pd.merge(
            referendum_df, extract_df, on="referendum_index", how="left"
        )
    referendum_df["ended_at"] = referendum_df["passed_at"].combine_first(
        referendum_df["notPassed_at"]
    )
    referendum_df["timespan"] = pd.to_datetime(
        referendum_df["ended_at"], unit="ms"
    ) - pd.to_datetime(referendum_df["started_at"], unit="ms")
    referendum_df["call_module"] = referendum_df["pre_image"].apply(
        lambda x: x.get("call_module") if type(x) == dict else None
    )
    referendum_df["call_name"] = referendum_df["pre_image"].apply(
        lambda x: x.get("call_name") if type(x) == dict else None
    )
    for col in referendum_columns_convert_to_int:
        referendum_df[col] = referendum_df[col].astype("int")
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
    idx = votes_df.groupby(['referendum_index', 'account.address'])[
              'voting_time'].transform(max) == votes_df['voting_time']
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
    print(mongodb_url)
    db_name = os.getenv("DB_NAME")
    # table_name = "vote"
    table_name = os.getenv("TABLE_NAME")
    df = load_data(mongodb_url=mongodb_url, db_name=db_name, table_name=table_name)
    # df = pd.read_csv('test_data.csv')
    # votes_df = preprocessing_votes(df)
    referendum_df = preprocessing_referendum(df)
    print(1)
