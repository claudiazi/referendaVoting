import datetime
import re
import pandas as pd
from pymongo import MongoClient
from config import referendum_columns, votes_columns


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
    referendum_df = referendum_df[referendum_df["status"].isin(["executed", "passed", "notPassed"])]
    timeline_df = referendum_df.explode("timeline")
    timeline_df["status"] = timeline_df["timeline"].apply(lambda x: x.get("status"))
    timeline_df = timeline_df[["referendum_index", "status", "timeline"]]
    for status in ["started", "passed", "notPassed"]:
        extract_df = extract_status_time(timeline_df, status)
        referendum_df = pd.merge(
            referendum_df, extract_df, on="referendum_index", how="left"
        )
    referendum_df["ended_at"] = referendum_df["passed_at"].combine_first(referendum_df["notPassed_at"])
    referendum_df["timespan"] = pd.to_datetime(referendum_df["ended_at"], unit="ms") - pd.to_datetime(referendum_df["started_at"], unit="ms")
    referendum_df['call_module'] = referendum_df['pre_image'].apply(lambda x: x.get('call_module') if type(x) == dict else None)
    # referendum_df['call_name'] = referendum_df['pre_image'].apply(lambda x: x.get('call_name'))
    # referendum_df["turnout_perc"] = referendum_df["turnout"] / referendum_df["total_issuance"]
    # referendum_df["avg_aye_conviction_rate"] = referendum_df["aye_without_conviction"] / referendum_df["aye_amount"]
    # referendum_df["avg_nay_conviction_rate"] = referendum_df["nay_without_conviction"] / referendum_df["nay_amount"]
    return referendum_df


def preprocessing_votes(df: pd.DataFrame) -> pd.DataFrame:
    df = df[votes_columns]
    df = df[df.votes.notnull()]
    df = df.explode("votes")
    df = pd.concat([df, df.votes.apply(pd.Series)], axis=1)
    # df["total_issuance"] = df["total_issuance"].astype(str).astype(float)
    # df["balance"] = df["balance"].astype(str).astype(float)
    # df["id"] = df["id"].astype(int)
    df["voted_ksm"] = pd.to_numeric(df["balance"]).apply(lambda x: x / 1000000000000)
    df["conviction"] = df["conviction"].apply(
        lambda x: 0.1 if x == "None" else int(re.search("\d", x).group())
    )
    df["locked_amount"] = round(df["voted_ksm"] * df["conviction"], 4)
    df["time"] = pd.to_datetime(df["time"], unit="ms").dt.strftime("%Y-%m-%d")
    df = df.drop("votes", axis=1)
    return df


if __name__ == "__main__":
    import os

    mongodb_url = os.getenv("MONGODB_URL")
    print(mongodb_url)
    db_name = os.getenv("DB_NAME")
    table_name = os.getenv("TABLE_NAME")
    df = load_data(mongodb_url=mongodb_url, db_name=db_name, table_name=table_name)
    referendum_df = preprocessing_referendum(df)
    print(1)
