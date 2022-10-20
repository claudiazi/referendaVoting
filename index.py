import json
import time
import warnings

import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import datetime
from app import app
from tabs import tab_1, tab_2, tab_3
from utils.data_preparation import (
    preprocessing_referendum,
    preprocessing_votes,
)
import requests
from substrateinterface import SubstrateInterface


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.H1("Kusama Governance Dashboard"),
        ],
    )


def build_tabs():
    return dcc.Tabs(
        id="app-tabs",
        value="tab1",
        className="custom-tabs",
        children=[
            dcc.Tab(
                id="Main-tab",
                label="Main Dashboard",
                value="tab1",
                className="custom-tab",
                selected_className="custom-tab--selected",
                disabled_style={
                    "backgroundColor": "#2d3038",
                    "color": "#95969A",
                    "borderColor": "#23262E",
                    "display": "flex",
                    "flex-direction": "column",
                    "alignItems": "center",
                    "justifyContent": "center",
                },
                disabled=False,
            ),
            dcc.Tab(
                id="Referendum-tab",
                label="Single Referendum View",
                value="tab2",
                className="custom-tab",
                selected_className="custom-tab--selected",
                disabled_style={
                    "backgroundColor": "#2d3038",
                    "color": "#95969A",
                    "borderColor": "#23262E",
                    "display": "flex",
                    "flex-direction": "column",
                    "alignItems": "center",
                    "justifyContent": "center",
                },
                disabled=False,
            ),
            dcc.Tab(
                id="Single-account-tab",
                label="Single Account View",
                value="tab3",
                className="custom-tab",
                selected_className="custom-tab--selected",
                disabled_style={
                    "backgroundColor": "#2d3038",
                    "color": "#95969A",
                    "borderColor": "#23262E",
                    "display": "flex",
                    "flex-direction": "column",
                    "alignItems": "center",
                    "justifyContent": "center",
                },
                disabled=False,
            ),
        ],
    )


subsquid_endpoint = "https://squid.subsquid.io/referenda-dashboard/v/1/graphql"

server = app.server
app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=0,
            disabled=True,
        ),
        dcc.Interval(
            id="interval-component-live",
            interval=300,  # in milliseconds
            n_intervals=0,
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                html.Div(id="app-content"),
            ],
        ),
        # Main app
        dcc.Store(
            id="full-referenda-data",
            data=[],
            storage_type="memory",
        ),
        dcc.Store(
            id="ongoing-referenda-data",
            data=[],
            storage_type="memory",
        ),
    ],
)

def load_current_block():
    # substrate = SubstrateInterface(
    #     url="wss://kusama-rpc.polkadot.io", ss58_format=2, type_registry_preset="kusama"
    # )
    # current_block = substrate.get_block()["header"]["number"]
    query = f"""query MyQuery {{
                     squidStatus {{
                        height
                     }}
                }}"""
    current_block = requests.post(subsquid_endpoint, json={"query": query}).text
    return json.loads(current_block)["data"]["squidStatus"]["height"]


current_block = load_current_block()


def load_referenda_stats():
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
                        count_validator
                        count_coucillor
                        count_normal
                        voted_amount_validator
                        voted_amount_coucillor
                        voted_amount_normal
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


@app.callback(
    [
        Output("full-referenda-data", "data"),
        Output("ongoing-referenda-data", "data"),
    ],
    [Input("interval-component", "n_intervals")],
)
def update_historical_data(n_intervals):
    if n_intervals >= 0:
        (
            full_referenda_data,
            ongoing_referenda_data,
        ) = load_referenda_stats()
        return full_referenda_data, ongoing_referenda_data


@app.callback(Output("app-content", "children"), Input("app-tabs", "value"))
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return tab_1.layout
    if tab_switch == "tab2":
        return tab_2.layout
    return tab_3.layout


# # Running the server
if __name__ == "__main__":
    warnings.filterwarnings(action="ignore")
    app.run_server(port=8088, debug=True)
