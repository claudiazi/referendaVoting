import datetime
import json
import time

import pandas as pd
import requests

subsquid_endpoint = "https://squid.subsquid.io/referenda-dashboard/v/v2/graphql"
polkassembly_graphql_endpoint = "https://kusama.polkassembly.io/v1/graphql"


def load_current_block():
    query = f"""query MyQuery {{
                     squidStatus {{
                        height
                     }}
                }}"""
    current_block = requests.post(subsquid_endpoint, json={"query": query}).text
    return json.loads(current_block)["data"]["squidStatus"]["height"]


def load_referenda_stats_gov1(current_block):
    query = f"""query MyQuery {{
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
                        voted_amount_with_conviction_aye
                        voted_amount_with_conviction_nay
                        voted_amount_with_conviction_total
                        voted_amount_with_conviction_direct
                        voted_amount_with_conviction_delegated
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
                        count_validator
                        count_councillor
                        count_normal
                        voted_amount_with_conviction_validator
                        voted_amount_with_conviction_councillor
                        voted_amount_with_conviction_normal
                     }}
                }}"""
    print("start to load")
    start_time = time.time()
    referenda_data = requests.post(subsquid_endpoint, json={"query": query}).text
    referenda_data = json.loads(referenda_data)
    df = pd.DataFrame.from_dict(referenda_data["data"]["referendaStats"])
    print(f"finish loading referenda_stats {time.time() - start_time}")
    df["ends_at"] = df.apply(
        lambda x: datetime.datetime.now()
        + datetime.timedelta(seconds=(x["ends_at"] - current_block) * 6)
        if not x["ended_at"]
        else None,
        axis=1,
    )
    df["executes_at"] = df.apply(
        lambda x: x["ends_at"] + datetime.timedelta(seconds=x["delay"] * 6)
        if not x["ended_at"]
        else None,
        axis=1,
    )
    df = df.sort_values("referendum_index")
    df_ongoing = df[df["ended_at"].isnull()].sort_values("referendum_index")
    return (
        df.to_dict("record"),
        df_ongoing.to_dict("record"),
    )


def load_referenda_stats_gov2():
    query = f"""query MyQuery {{
                     gov2referendaStats {{
                        referendum_index
                        status
                        created_at
                        passed_at
                        not_passed_at
                        cancelled_at
                        ended_at
                        count_aye
                        count_nay
                        count_total
                        referendum_ayes
                        referendum_nays
                        count_direct
                        count_delegated
                        voted_amount_aye
                        voted_amount_nay
                        voted_amount_total
                        voted_amount_with_conviction_aye
                        voted_amount_with_conviction_nay
                        voted_amount_with_conviction_total
                        voted_amount_with_conviction_direct
                        voted_amount_with_conviction_delegated    
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
                        decision_deposit_who
                        decision_deposit_amount
                        submission_deposit_who
                        submission_deposit_amount
                        method
                        section
                        count_quiz_attended_wallets
                        count_fully_correct
                        quiz_fully_correct_perc
                        count_1_question_correct_perc
                        count_2_question_correct_perc
                        count_3_question_correct_perc
                        count_validator
                        count_normal
                        voted_amount_with_conviction_validator
                        voted_amount_with_conviction_normal
                         }}
                }}"""
    print("start to load")
    start_time = time.time()
    referenda_data = requests.post(subsquid_endpoint, json={"query": query}).text
    referenda_data = json.loads(referenda_data)
    df = pd.DataFrame.from_dict(referenda_data["data"]["gov2referendaStats"])
    print(f"finish loading referenda_stats {time.time() - start_time}")
    df = df.sort_values("referendum_index")
    df_ongoing = df[df["ended_at"].isnull()].sort_values("referendum_index")
    return (
        df.to_dict("record"),
        df_ongoing.to_dict("record"),
    )


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


def load_pa_description(referendum_index):
    query = f"""query MyQuery {{
          posts(where: {{onchain_link: {{onchain_referendum_id: {{_eq: {referendum_index}}}}}}}) {{
            content
            created_at
            title
            onchain_link {{
                onchain_referendum_id
            }}
          }}
        }}
        """
    print("start to load specific referedum pa description")
    start_time = time.time()
    pa_data = requests.post(polkassembly_graphql_endpoint, json={"query": query}).text
    pa_data = json.loads(pa_data)
    df_pa_description = pd.DataFrame.from_dict(pa_data["data"]["posts"])
    print(f"finish loading referedum pa description {time.time() - start_time}")
    return df_pa_description


def load_refereundum_votes(referendum_index):
    query = f"""query MyQuery {{
                  referendumVotes(id: {referendum_index}) {{
                    voter
                    referendum_index
                    timestamp
                    cum_voted_amount_with_conviction_aye
                    cum_voted_amount_with_conviction_nay
                }}
            }}

        """
    print("start to load specific referedum votes")
    start_time = time.time()
    votes_data = requests.post(subsquid_endpoint, json={"query": query}).text
    votes_data = json.loads(votes_data)
    df_votes = pd.DataFrame.from_dict(votes_data["data"]["referendumVotes"])
    df_votes = df_votes.sort_values("timestamp")
    print(f"finish loading referedum votes {time.time() - start_time}")
    return df_votes


def load_specific_referendum_stats(referendum_index):
    query = f"""query MyQuery  {{
                referendumStats(id: {referendum_index}) {{
                    cum_new_accounts
                    decision
                    is_new_account
                    referendum_index
                    timestamp
                    voted_amount_with_conviction
                    voter
                    delegated_to
                   }}
                }}"""
    print("start to load specific referedum stats")
    start_time = time.time()
    referendum_data = requests.post(subsquid_endpoint, json={"query": query}).text
    referendum_data = json.loads(referendum_data)
    df_referendum = pd.DataFrame.from_dict(referendum_data["data"]["referendumStats"])
    df_referendum = df_referendum.sort_values("timestamp")
    print(f"finish loading referendum_stats {time.time() - start_time}")
    return df_referendum


def load_specific_account_stats(voter):
    query = f"""query MyQuery {{
                  accountStats(address: "{voter}") {{
                    referendum_index
                    balance_value
                    conviction
                    decision
                    first_referendum_index
                    first_voting_timestamp
                    voted_amount_with_conviction
                    voter
                    voting_result_group
                    voting_time_group
                    questions_count
                    correct_answers_count
                    quiz_fully_correct
                    voter_type
                    delegated_to
                    type   
                  }}
                }}"""
    print("start to load specific account stats")
    start_time = time.time()
    account_data = requests.post(subsquid_endpoint, json={"query": query}).text
    account_data = json.loads(account_data)
    df_account = pd.DataFrame.from_dict(account_data["data"]["accountStats"])
    df_account = df_account.sort_values("referendum_index")
    print(f"finish loading account_stats {time.time() - start_time}")
    return df_account


def load_delegation_data():
    query = f"""query MyQuery {{
                  delegations {{
                    wallet
                    to
                    timestamp
                    timestampEnd
                    blockNumberStart
                    blockNumberEnd
                    balance
                    lockPeriod
                  }}
                }}"""
    print("start to load delegation data")
    start_time = time.time()
    delegation_data = requests.post(subsquid_endpoint, json={"query": query}).text
    delegation_data = json.loads(delegation_data)
    df_delegation = pd.DataFrame.from_dict(delegation_data["data"]["delegations"])
    df_delegation = df_delegation[df_delegation["balance"].notnull()]
    df_delegation["conviction"] = df_delegation["lockPeriod"].apply(
        lambda x: 0.1 if x == 0 else x
    )
    df_delegation["voted_amount"] = round(
        df_delegation["conviction"]
        * df_delegation["balance"].astype(int)
        / 1000000000000,
        2,
    )
    df_delegation = df_delegation.rename(
        {
            "timestamp": "delegation_started_at",
            "timestampEnd": "delegation_ended_at",
            "to": "delegated_to",
        },
        axis=1,
    )
    df_delegation = df_delegation[
        [
            "wallet",
            "delegated_to",
            "delegation_started_at",
            "delegation_ended_at",
            "voted_amount",
            "balance",
            "conviction",
        ]
    ]
    print(f"finish loading delegation data {time.time() - start_time}")
    return df_delegation


if __name__ == "__main__":
    current_block = load_current_block()
    dict_all, dict_ongoing = load_referenda_stats_gov1(current_block)
    df_specific = load_specific_referendum_stats(211)
    df_account = load_specific_account_stats(
        "Eakn18SoWyCLE7o3hc23MABqMtNayE4nqNckpznSSZZgWFC"
    )
    df_delegation = load_delegation_data()
