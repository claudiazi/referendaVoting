import time
import requests
import pandas as pd
from pandasql import sqldf
from substrateinterface import SubstrateInterface
import json
from config import (
    referendum_columns,
    votes_columns,
    ongoing_refenrenda_columns,
    referendum_columns_convert_to_int,
    votes_columns_convert_to_float,
)
from multiprocessing.pool import ThreadPool

def load_data():
    subSquid_endpoint = "https://squid.subsquid.io/proof-of-chaos-test/v/0/graphql"

    queryStats = f"""
    query MyQuery {{
      referendumStats {{
        referendum_id
        conviction_mean
        conviction_mean_aye
        conviction_mean_nay
        conviction_median
        conviction_median_aye
        conviction_median_nay
        count_aye
        count_nay
        count_new
        count_new_perc
        count_total
        created_at
        ended_at
        index
        method
        proposer
        section
        status
        total_issuance
        turnout_aye_perc
        turnout_nay_perc
        turnout_total_perc
        vote_duration
        voted_amount_aye
        voted_amount_nay
        voted_amount_total
      }}
    }}
    """
    return requests.post(subSquid_endpoint, json={"query": queryStats}).text

# def execute():
#     start_time = time.time()
#     pool_cores = 200
#     index = range(230)
#     pool = ThreadPool(pool_cores)
#     deal_updates_df = pool.map(load_data,index)
#     #
#     read_time = time.time()
#     print(f"data has been loaded {(read_time - start_time):.2f}s")
#     # with open("referenda.json", "w") as f:
#     #     f.write(r.text)
#     # print(f"data has been loaded {(time.time() - read_time):.2f}s")
#     return deal_updates_df

def preprocessing_referendum() -> pd.DataFrame:
    with open("./referenda.json", "r") as f:
        data = json.loads(f.read())
    df_referendum = pd.json_normalize(data["data"]["proposals"])
    #
    # referendum_df["has_passed"] = referendum_df["status"].apply(
    #     lambda x: "t"
    #     if x in ["executed", "Passed"]
    #     else ("wip" if x == "started" else "f")
    # )
    # referendum_df = referendum_df[referendum_df["has_passed"].isin(["t", "f"])]
    # referendum_df = referendum_df.rename(
    #     columns={
    #         "pre_image_author_address": "author_address",
    #         "pre_image_call_module": "call_module",
    #         "pre_image_call_name": "call_name",
    #     }
    # )
    #
    # for col in referendum_columns_convert_to_int:
    #     referendum_df[col] = referendum_df[col].apply(
    #         lambda x: int(x) if x is not None and x != "NULL" else None
    #     )
    # referendum_df["turnout_perc"] = (
    #     referendum_df["turnout"] / referendum_df["total_issuance"]
    # )
    # referendum_df["avg_aye_conviction_rate"] = (
    #     referendum_df["aye_without_conviction"] / referendum_df["aye_amount"]
    # )
    # referendum_df["avg_nay_conviction_rate"] = (
    #     referendum_df["nay_without_conviction"] / referendum_df["nay_amount"]
    # )
    # referendum_df["duration"] = referendum_df["duration"] / (60 * 60 * 24)
    return df_referendum


def preprocessing_votes() -> pd.DataFrame:
    with open("./referenda.json", "r") as f:
        data = json.loads(f.read())
    df_votes = pd.json_normalize(data["data"]["proposals"], record_path=["voting"], meta=["index"])
    # idx = (
    #     votes_df.groupby(["referendum_index", "account_address"])[
    #         "voting_time"
    #     ].transform(max)
    #     == votes_df["voting_time"]
    # )
    # votes_df = votes_df[idx]
    # for col in votes_columns_convert_to_float:
    #     votes_df[col] = votes_df[col].astype("float")
    # votes_df["vote_amount_without_conviction"] = votes_df["amount"].apply(
    #     lambda x: x / 1000000000000
    # )
    # votes_df["vote_amount_with_conviction"] = round(
    #     votes_df["vote_amount_without_conviction"] * votes_df["conviction"], 4
    # )
    # votes_df["voting_time"] = pd.to_datetime(
    #     votes_df["voting_time"], unit="s"
    # ).dt.strftime("%Y-%m-%d")
    return df_votes


def get_df_new_accounts(dict_referendum: pd.DataFrame, dict_votes: pd.DataFrame):
    global df_first_votes
    global df_all_votes
    df_first_votes = pd.DataFrame(dict_referendum)
    df_all_votes = pd.DataFrame(dict_votes)
    df_first_votes = (
        df_all_votes.groupby("account_address")
        .agg(first_referendum_index=("referendum_index", "min"))
        .reset_index()
    )
    pysqldf = lambda q: sqldf(q, globals())
    query = """
        with first_referendum as (
        
            select 
              first_referendum_index as referendum_index
            , count(distinct account_address) as new_accounts
            from df_first_votes
            group by 1
            
        )
        
        , all_referendum as (
        
            select 
            referendum_index
            , count(distinct account_address) as all_votes
            from df_all_votes
            group by 1
        )
        
        select 
        referendum_index
        , new_accounts
        , all_votes
        , ifnull(new_accounts * 1.0 / all_votes, 0) as perc_new_accounts
        from all_referendum
        left join first_referendum
            using(referendum_index)
    """
    df_new_counts = pysqldf(query)
    return df_new_counts


def get_substrate_live_data() -> pd.DataFrame:
    substrate = SubstrateInterface(
        url="wss://kusama-rpc.polkadot.io", ss58_format=2, type_registry_preset="kusama"
    )
    # lowest unbaked
    lowest_unbaked = substrate.query(
        module="Democracy", storage_function="LowestUnbaked"
    )

    # highest unbaked
    highest_unbaked = substrate.query(
        module="Democracy", storage_function="ReferendumCount"
    )

    unbaked = range(int(str(lowest_unbaked)), int(str(highest_unbaked)))

    ongoing_referenda = []

    for referendum in unbaked:
        result = substrate.query(
            module="Democracy", storage_function="ReferendumInfoOf", params=[referendum]
        )
        if "Ongoing" in result.value.keys():
            result_dict = result.value["Ongoing"]
            result_dict.update({'referendum_index': referendum})
            ongoing_referenda.append(result_dict)
    df_ongoing_referenda = pd.DataFrame(ongoing_referenda)
    df_ongoing_referenda = pd.concat(
        [
            df_ongoing_referenda.drop(["tally"], axis=1),
            df_ongoing_referenda["tally"].apply(pd.Series),
        ],
        axis=1,
    )
    df_ongoing_referenda['ayes_perc'] = df_ongoing_referenda['ayes'] / (df_ongoing_referenda['ayes'] + df_ongoing_referenda['nays'])
    df_ongoing_referenda = df_ongoing_referenda[ongoing_refenrenda_columns]
    return df_ongoing_referenda


if __name__ == "__main__":
    import os

    # mongodb_url = os.getenv("MONGODB_URL")
    # db_name = os.getenv("DB_NAME")
    # table_name = "vote"
    # df_referendum = pd.read_csv('referendum_data.csv')
    # a=load_data(100)

    # df = execute()
    # load_data()
    df_referendum = preprocessing_referendum()
    df_votes = preprocessing_votes()
    # df_ongoing_referenda = get_substrate_live_data()
    # table_name = os.getenv("TABLE_NAME")
    # df = load_data(mongodb_url=mongodb_url, db_name=db_name, table_name=table_name)
    # df_votes = pd.read_csv('votes_data.csv')
    # df_votes = preprocessing_votes(df_votes)
    # df_referendum = preprocessing_referendum(df_referendum)
    # df_new_accounts = get_df_new_accounts(df_referendum, df_votes)
    # print(df_ongoing_referenda)
    print(1)
