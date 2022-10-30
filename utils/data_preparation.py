import time

import pandas as pd
from pandasql import sqldf
from pymongo import MongoClient
from substrateinterface import SubstrateInterface

import json
from config import (
    referendum_columns,
    votes_columns,
    ongoing_refenrenda_columns,
    referendum_columns_convert_to_int,
    votes_columns_convert_to_float,
)
import requests


def filter_referenda(
    df_referenda: pd.DataFrame,
    selected_ids,
    selected_section,
    selected_method,
    selected_proposer,
) -> pd.DataFrame:
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    if selected_section:
        if selected_section != "All":
            df_referenda = df_referenda[df_referenda["section"] == selected_section]
    if selected_method:
        if selected_method != "All":
            df_referenda = df_referenda[df_referenda["method"] == selected_method]
    if selected_proposer:
        if selected_proposer != "All":
            df_referenda = df_referenda[df_referenda["proposer"] == selected_proposer]
    return df_referenda


def preprocessing_referendum(df: pd.DataFrame) -> pd.DataFrame:
    referendum_df = df[referendum_columns]
    referendum_df["has_passed"] = referendum_df["status"].apply(
        lambda x: "t"
        if x in ["executed", "Passed"]
        else ("wip" if x == "started" else "f")
    )
    referendum_df = referendum_df[referendum_df["has_passed"].isin(["t", "f"])]
    referendum_df = referendum_df.rename(
        columns={
            "pre_image_author_address": "author_address",
            "pre_image_call_module": "call_module",
            "pre_image_call_name": "call_name",
        }
    )

    for col in referendum_columns_convert_to_int:
        referendum_df[col] = referendum_df[col].apply(
            lambda x: int(x) / 1000000000000 if x is not None and x != "NULL" else None
        )
    referendum_df["turnout_perc"] = (
        referendum_df["turnout"] / referendum_df["total_issuance"]
    )
    referendum_df["aye_turnout_perc"] = (
        referendum_df["aye_amount"] / referendum_df["total_issuance"]
    )
    referendum_df["nay_turnout_perc"] = (
        referendum_df["nay_amount"] / referendum_df["total_issuance"]
    )
    referendum_df["avg_aye_conviction_rate"] = (
        referendum_df["aye_without_conviction"] / referendum_df["aye_amount"]
    )
    referendum_df["avg_nay_conviction_rate"] = (
        referendum_df["nay_without_conviction"] / referendum_df["nay_amount"]
    )
    referendum_df["duration"] = referendum_df["duration"] / (60 * 60 * 24)
    referendum_df["duration_1_4"] = referendum_df["duration"] / 4
    referendum_df["duration_1_2"] = referendum_df["duration"] / 2
    referendum_df["duration_3_4"] = referendum_df["duration"] * 3 / 4

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
    votes_df["vote_amount_without_conviction"] = votes_df["amount"].apply(
        lambda x: x / 1000000000000
    )
    votes_df["vote_amount_with_conviction"] = round(
        votes_df["vote_amount_without_conviction"] * votes_df["conviction"], 4
    )
    votes_df["voting_time"] = pd.to_datetime(votes_df["voting_time"], unit="s")
    return votes_df


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


def get_df_voting_time(dict_referendum: pd.DataFrame, dict_votes: pd.DataFrame):
    global df_referenda
    global df_votes
    df_referenda = pd.DataFrame(dict_referendum)
    df_votes = pd.DataFrame(dict_votes)
    pysqldf = lambda q: sqldf(q, globals())
    query = """
        with first_vote as (
            select referendum_index
            , min(voting_time) as started_at
            from df_votes
            group by 1
        ),
        
        grouping as (
            select account_address
            , referendum_index
            , voting_time - started_at
            , voting_time
            , started_at
            , case when JULIANDAY(voting_time) - JULIANDAY(started_at) < duration_1_4
                        then '- 1/4 vote duration'
                   when JULIANDAY(voting_time) - JULIANDAY(started_at) >= duration_1_4
                        and JULIANDAY(voting_time) - JULIANDAY(started_at) < duration_1_2
                        then '1/4 vote duration - 1/2 vote duration'
                   when JULIANDAY(voting_time) - JULIANDAY(started_at) >= duration_1_2
                        and JULIANDAY(voting_time) - JULIANDAY(started_at) < duration_3_4
                        then '1/2 vote duration - 3/4 vote duration'
                   else '3/4 vote duration -'
              end as voting_time_group
            from df_votes
            inner join first_vote 
                using (referendum_index)
            inner join df_referenda
                using (referendum_index)
        )      
         
        select 
          referendum_index
        , voting_time_group
        , count(distinct account_address)
        from grouping
        group by 1,2
    """
    df_voting_time = pysqldf(query)
    return df_voting_time


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
            result_dict.update({"referendum_index": referendum})
            ongoing_referenda.append(result_dict)
    df_ongoing_referenda = pd.DataFrame(ongoing_referenda)
    df_ongoing_referenda = pd.concat(
        [
            df_ongoing_referenda.drop(["tally"], axis=1),
            df_ongoing_referenda["tally"].apply(pd.Series),
        ],
        axis=1,
    )
    df_ongoing_referenda["ayes_perc"] = df_ongoing_referenda["ayes"] / (
        df_ongoing_referenda["ayes"] + df_ongoing_referenda["nays"]
    )
    df_ongoing_referenda = df_ongoing_referenda[ongoing_refenrenda_columns]
    return df_ongoing_referenda


def load_referendum_index():
    query = f"""
    query MyQuery {{
        referendaStats {{
        referendum_index
      }}
    }}
    """
    print("start to load")
    start_time = time.time()
    data = requests.post(subsquid_endpoint, json={"query": query}).text
    print(f"finish loading {time.time() - start_time}")
    return data

def subsquid_to_df(stats_name: str, query: str, var: str = None):
    start_time = time.time()
    data = requests.post(subsquid_endpoint, json={"query": query}).text
    print(f"finish loading {stats_name} {time.time() - start_time}")
    df = pd.DataFrame(data)
    print(df.head())
    return df





subsquid_endpoint = "https://squid.subsquid.io/referenda-dashboard/v/0/graphql"

def load_referenda_data():
    query = f"""
    query MyQuery {{
      referendaStats {{
   referendum_index
                        status
                        created_at
                        not_passed_at
                        passed_at
                        executed_at
                        cancelled_at
                        ended_at
                        ends_at
                        delay
                        count_aye
                        count_nay
                        count_total
                        count_direct
                        count_delegated
                        voted_amount_aye
                        voted_amount_nay
                        voted_amount_total
                        voted_amount_direct
                        voted_amount_delegated
                        total_issuance
                        turnout_aye_perc
                        turnout_nay_perc
                        turnout_total_perc
                        count_new
                        count_new_perc
                        conviction_mean_aye
                        conviction_mean_nay
                        conviction_mean
                        conviction_median_aye
                        conviction_median_nay
                        conviction_median
                        vote_duration
                        count_0_4_1_4_vote_duration
                        count_1_4_2_4_vote_duration
                        count_2_4_3_4_vote_duration
                        count_3_4_4_4_vote_duration
                        count_0_4_1_4_vote_duration_perc
                        count_1_4_2_4_vote_duration_perc
                        count_2_4_3_4_vote_duration_perc
                        count_3_4_4_4_vote_duration_perc
                        threshold_type
                        proposer
                        method
                        section
                        count_quiz_attended_wallets
                        count_fully_correct
                        quiz_fully_correct_perc
                        count_1_question_correct_perc
                        count_2_question_correct_perc
                        count_3_question_correct_perc
      }}
    }}
    """
    start_time = time.time()
    referenda_data = requests.post(subsquid_endpoint, json={"query": query}).text
    referenda_data = json.loads(referenda_data)
    df = pd.DataFrame.from_dict(referenda_data["data"]["referendaStats"])
    print(f"finish loading referenda_stats {time.time() - start_time}")
    return df


def load_specific_referendum_stats(referendum_index):
    query = f"""query MyQuery  {{
                referendumStats(id: {referendum_index}) {{
                    cum_new_accounts
                    cum_voted_amount_with_conviction_aye
                    cum_voted_amount_with_conviction_nay
                    decision
                    is_new_account
                    referendum_index
                    timestamp
                    voted_amount_with_conviction
                    voter
                   }}
                }}"""
    print("start to load specific referedum stats")
    start_time = time.time()
    referendum_data = requests.post(subsquid_endpoint, json={"query": query}).text
    referendum_data = json.loads(referendum_data)
    df_referendum = pd.DataFrame.from_dict(referendum_data["data"]["referendumStats"])
    print(f"finish loading referendum_stats {time.time() - start_time}")
    return df_referendum

def load_specific_account_stats(voter):
    query = f"""query MyQuery {{
                  accountStats(address: "{voter}") {{
                    balance_value
                    conviction
                    decision
                    first_referendum_index
                    first_voting_timestamp
                    referendum_index
                    voted_amount_with_conviction
                    voter
                    voting_result_group
                    voting_time_group
                  }}
                }}"""
    print("start to load specific account stats")
    start_time = time.time()
    account_data = requests.post(subsquid_endpoint, json={"query": query}).text
    account_data = json.loads(account_data)
    print(account_data)
    df_account = pd.DataFrame.from_dict(account_data["data"]["accountStats"])
    df_account = df_account.sort_values("referendum_index")
    print(f"finish loading account_stats {time.time() - start_time}")
    return df_account


if __name__ == "__main__":
    import os

    df = load_referenda_data()
    df_specific = load_specific_referendum_stats(211)
    df_account = load_specific_account_stats("Eakn18SoWyCLE7o3hc23MABqMtNayE4nqNckpznSSZZgWFC")
    mongodb_url = os.getenv("MONGODB_URL")
    db_name = os.getenv("DB_NAME")
    table_name = "vote"
    df_votes = pd.read_csv("votes_data.csv")
    df_votes = preprocessing_votes(df_votes)
    df_referendum = pd.read_csv("referendum_data.csv")
    df_referendum = preprocessing_referendum(df_referendum)
    df_ongoing_referenda = get_substrate_live_data()
    # table_name = os.getenv("TABLE_NAME")
    # df = load_data(mongodb_url=mongodb_url, db_name=db_name, table_name=table_name)

    # df_referendum = preprocessing_referendum(df_referendum)
    # df_new_accounts = get_df_new_accounts(df_referendum, df_votes)
    print(df_ongoing_referenda)
    print(1)
