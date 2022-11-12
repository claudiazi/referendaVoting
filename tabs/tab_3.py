from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
from app import app
import time
import json
import requests
from utils.plotting import blank_figure
import dash_daq as daq
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from config import voting_group_dict, voting_group_perc_dict, voting_group_colors
from dash import dash_table


import plotly.express as px

subsquid_endpoint = "https://squid.subsquid.io/referenda-dashboard/v/0/graphql"


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


def build_tab_3():
    return [
        html.Div(
            children=[
                html.Div(
                    className="twelve columns section-banner",
                    children=[
                        html.Div(
                            className="twelve columns",
                            children=[
                                dcc.Input(
                                    id="account_input",
                                    placeholder="Type in Account Address",
                                    style={
                                        "width": "70%",
                                        "float": "middle",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "padding": 5,
                                "justifyContent": "center",
                            },
                        ),
                        html.Div(
                            className="twelve columns",
                            id="account_input_warning",
                            children=[],
                        ),
                        html.Div(
                            className="twelve columns",
                            children=[
                                html.Button(
                                    "Confirm",
                                    id="account-trigger-btn",
                                    className="click-button",
                                    n_clicks=0,
                                    style={
                                        "display": "inline-block",
                                        "float": "middle",
                                    },
                                )
                            ],
                            style={
                                "display": "flex",
                                "padding": 5,
                                "justifyContent": "center",
                            },
                        ),
                    ],
                )
            ]
        ),
        html.Div(className="twelve columns", id="tab3_charts", children=[]),
        dcc.Store(id="specific-account-data", data=[], storage_type="memory"),
        dcc.Store(id="delegation-data", data=[], storage_type="memory"),
    ]


def build_charts():
    return [
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            className="twelve columns",
            id="tab3_card_row_1",
            children=[],
        ),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            className="twelve columns",
            id="tab3_card_row_2",
            children=[],
        ),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            className="twelve columns",
            id="tab3_card_row_3",
            children=[],
        ),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            className="twelve columns",
            children=[
                html.Div(
                    className="six columns graph-block",
                    children=[
                        html.Div(
                            id="first-chart",
                            className="twelve columns",
                            children=[
                                    html.Div(
                                    className="twelve columns",
                                    children=[
                                        html.Div(
                                            className="twelve columns",
                                            children=[
                                                daq.ToggleSwitch(
                                                    id="votes_split_selection",
                                                    label=["Decision", "Outcome"],
                                                    value=True,
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="second-chart",
                                    className="twelve columns",
                                    children=[
                                        dcc.Loading(
                                            id="loading-icon",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="voted_amount_barchart",
                                                        figure=blank_figure(),
                                                    )
                                                )
                                            ],
                                            type="default",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="six columns graph-block",
                    children=[
                        html.Div(
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(
                                            dcc.Graph(
                                                id="voting_time_distribution",
                                                figure=blank_figure(),
                                            )
                                        )
                                    ],
                                    type="default",
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="twelve columns",
            children=[
                html.Div(
                    className="six columns graph-block",
                    children=[
                        html.Div(
                            id="iii-chart",
                            className="twelve columns",
                            children=[
                                html.Div(
                                    className="twelve columns",
                                    children=[
                                        dcc.Loading(
                                            id="loading-icon",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="delegate_to_chart",
                                                        figure=blank_figure(),
                                                    )
                                                )
                                            ],
                                            type="default",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="six columns graph-block",
                    children=[
                        html.Div(
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(
                                            dcc.Graph(
                                                id="delegated_chart",
                                                figure=blank_figure(),
                                            )
                                        )
                                    ],
                                    type="default",
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="twelve columns",
            children=[
                html.Div(
                    className="six columns graph-block",
                    children=[
                        html.Div(
                            id="v-chart",
                            className="twelve columns",
                            children=[
                                html.Div(
                                    className="twelve columns",
                                    children=[
                                        dcc.Loading(
                                            id="loading-icon",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="voter-type-timeline-chart",
                                                        figure=blank_figure(),
                                                    )
                                                )
                                            ],
                                            type="default",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="six columns graph-block",
                    children=[
                        html.H6(children='Quiz Correctness'),
                        dcc.Loading(
                            html.Div(
                                id="quiz-correctness-table",
                                children=[],
                            )
                        )
                    ],
                ),
            ],
        ),
    ]


layout = build_tab_3()

# Callback to update the referendum df
@app.callback(
    [
        Output("specific-account-data", "data"),
        Output("delegation-data", "data"),
        Output("account_input_warning", "children"),
    ],
    [
        Input("account-trigger-btn", "n_clicks"),
        Input("account_input", "value"),
    ],
)
def update_specific_account_data(n_clicks, account_input):
    warning = None
    df_specific_account = pd.DataFrame()
    if account_input:
        try:
            df_specific_account = load_specific_account_stats(account_input)
            df_delegation = load_delegation_data()
        except:
            warning = html.P(className="alert alert-danger", children=["Invalid input"])
        if df_specific_account.empty:
            warning = html.P(className="alert alert-danger", children=["Invalid input"])
        return (
            df_specific_account.to_dict("record"),
            df_delegation.to_dict("record"),
            [warning],
        )
    return None, None, html.P()


@app.callback(
    output=Output("tab3_charts", "children"),
    inputs=[
        Input("account-trigger-btn", "n_clicks"),
        Input("account_input_warning", "children"),
    ],
)
def build_tab3_charts(n_clicks, input_warning):
    if input_warning == [None]:
        return build_charts()


@app.callback(
    output=Output("tab3_card_row_1", "children"),
    inputs=[
        Input("specific-account-data", "data"),
    ],
)
def update_card1(account_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        return [
            html.Div(
                className="four columns graph-block",
                id="card1",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4("First Vote", className="card-title"),
                                    html.P(
                                        f"Timestamp: {df_account['first_voting_timestamp'].unique()[0]}",
                                        className="card-value",
                                    ),
                                    html.P(
                                        f"Referendum ID: {df_account['first_referendum_index'].unique()[0]}",
                                        className="card-value",
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
            ),
            html.Div(
                className="four columns graph-block",
                id="card2",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4("# of Ref. Voted", className="card-title"),
                                    html.P(
                                        f"{df_account['referendum_index'].count()}",
                                        className="card-value",
                                    ),
                                    html.P(""),
                                ]
                            )
                        ]
                    ),
                ],
            ),
            html.Div(
                className="four columns graph-block",
                id="card3",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4("Avg. Voted KSM", className="card-title"),
                                    html.P(
                                        f"{df_account['voted_amount_with_conviction'].mean():.2f}",
                                        className="card-value",
                                    ),
                                    html.P(""),
                                ]
                            )
                        ]
                    ),
                ],
            ),
        ]

    return None


@app.callback(
    output=Output("tab3_card_row_2", "children"),
    inputs=[
        Input("specific-account-data", "data"),
        Input("delegation-data", "data"),
    ],
)
def update_card2(account_data, delegation_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_delegation = pd.DataFrame(delegation_data)
        df_delegated = df_delegation.merge(
            df_account, how="inner", left_on="delegated_to", right_on="voter"
        )
        df_delegate_to = df_delegation.merge(
            df_account, how="inner", left_on="wallet", right_on="voter"
        )
        active_delegate_to = df_delegate_to[
            df_delegate_to["delegation_ended_at"].isnull()
        ]["delegated_to_x"].unique()
        if not active_delegate_to:
            active_delegate_to = "None"
        count_active_delegated = len(
            df_delegated[df_delegated["delegation_ended_at"].isnull()][
                "wallet"
            ].unique()
        )
        return [
            html.Div(
                className="four columns graph-block",
                id="card1",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4(
                                        "# of Active delegations",
                                        className="card-title",
                                    ),
                                    html.P(
                                        count_active_delegated,
                                        className="card-value",
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
            ),
            html.Div(
                className="four columns graph-block",
                id="card2",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4(
                                        "Active delegate to",
                                        className="card-title",
                                    ),
                                    html.P(
                                        active_delegate_to,
                                        className="card-value",
                                    ),
                                    html.P(""),
                                ]
                            )
                        ]
                    ),
                ],
            ),
        ]

    return None


@app.callback(
    output=Output("tab3_card_row_3", "children"),
    inputs=[
        Input("specific-account-data", "data"),
    ],
)
def update_card3(account_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_quizzes = df_account[df_account.correct_answers_count.notnull()]
        return [
            html.Div(
                className="four columns graph-block",
                id="card1",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4(
                                        "# of Quizzes Taken", className="card-title"
                                    ),
                                    html.P(
                                        f"{df_quizzes['referendum_index'].count()}",
                                        className="card-value",
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
            ),
            html.Div(
                className="four columns graph-block",
                id="card2",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4(
                                        "# of Quizzes Fully Correct",
                                        className="card-title",
                                    ),
                                    html.P(
                                        f"{df_quizzes['quiz_fully_correct'].sum()}",
                                        className="card-value",
                                    ),
                                    html.P(""),
                                ]
                            )
                        ]
                    ),
                ],
            ),
        ]

    return None


@app.callback(
    output=Output("cum_voter_amount_barchart", "figure"),
    inputs=[Input("specific-referendum-data", "data")],
)
def cum_voter_amount_barchart(account_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        second_graph_data = [
            go.Scatter(
                name="Aye Votes",
                x=df_account["timestamp"],
                y=df_account["cum_voted_amount_with_conviction_aye"],
                mode="lines",
                # hovertemplate="<b>Aye Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Aye amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
            go.Scatter(
                name="Nay Votes",
                x=df_account["timestamp"],
                y=df_account["cum_voted_amount_with_conviction_nay"],
                mode="lines",
                # hovertemplate="<b>Nay Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Nay Amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
        ]

        second_graph_layout = go.Layout(
            title="<b>Cumulated Voted Amount</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Timestamp", linecolor="#BCCCDC"),
            yaxis=dict(title="Voted Amount with Conviction", linecolor="#021C1E"),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
            template="plotly_dark",
            hovermode="x",
        )
        fig_second_graph = go.Figure(data=second_graph_data, layout=second_graph_layout)
        return fig_second_graph
    return None


@app.callback(
    output=Output("voted_amount_barchart", "figure"),
    inputs=[
        Input("specific-account-data", "data"),
        Input("votes_split_selection", "value"),
    ],
)
def voter_amount_barchart(account_data, selected_votes_split):
    if account_data:
        df_account = pd.DataFrame(account_data)
        if selected_votes_split == False:
            df_aye = df_account[df_account["decision"] == "aye"]
            df_nay = df_account[df_account["decision"] == "nay"]
            first_graph_data = [
                go.Bar(
                    name="Aye Votes",
                    x=df_aye["referendum_index"],
                    y=df_aye["voted_amount_with_conviction"],
                    marker_color="#ffffff",
                    # hovertemplate="<b>Aye Votes</b><br><br>"
                    #               + "Referendum id: %{x:.1f}<br>"
                    #               + "Turnout perc - aye: %{y:.1f}<br>"
                    #               + "Turnout perc: %{custom
                    #               data:.1f}<br>"
                    #               + "<extra></extra>",
                ),
                go.Bar(
                    name="Nay Votes",
                    x=df_nay["referendum_index"],
                    y=df_nay["voted_amount_with_conviction"],
                    marker_color="#e6007a",
                    # hovertemplate="<b>Nay Votes</b><br><br>"
                    #               + "Referendum id: %{x:.2f}<br>"
                    #               + "Turnout perc - nay: %{y:.2f}<br>"
                    #               + "Turnout perc: %{customdata:.2f}<br>"
                    #               + "<extra></extra>",
                ),
            ]
        else:
            df_aligned = df_account[df_account["voting_result_group"] == "aligned"]
            df_not_aligned = df_account[
                df_account["voting_result_group"] == "not aligned"
            ]
            first_graph_data = [
                go.Bar(
                    name="Aligned with Final Result",
                    x=df_aligned["referendum_index"],
                    y=df_aligned["voted_amount_with_conviction"],
                    marker_color="#ffffff",
                    # hovertemplate="<b>Aye Votes</b><br><br>"
                    #               + "Referendum id: %{x:.1f}<br>"
                    #               + "Turnout perc - aye: %{y:.1f}<br>"
                    #               + "Turnout perc: %{customdata:.1f}<br>"
                    #               + "<extra></extra>",
                ),
                go.Bar(
                    name="Not Aligned with Final Result",
                    x=df_not_aligned["referendum_index"],
                    y=df_not_aligned["voted_amount_with_conviction"],
                    marker_color="#e6007a",
                    # hovertemplate="<b>Nay Votes</b><br><br>"
                    #               + "Referendum id: %{x:.2f}<br>"
                    #               + "Turnout perc - nay: %{y:.2f}<br>"
                    #               + "Turnout perc: %{customdata:.2f}<br>"
                    #               + "<extra></extra>",
                ),
            ]

        first_graph_layout = go.Layout(
            title="<b>Voted Amount</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Voted Amount with Conviction", linecolor="#021C1E"),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
            template="plotly_dark",
            hovermode="x",
        )
        fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
        fig_first_graph.update_traces(opacity=0.75)
        return fig_first_graph
    return None


@app.callback(
    Output("voting_time_distribution", "figure"),
    Input("specific-account-data", "data"),
)
def update_vote_timing_distribution(account_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_voting_group_sum = df_account.groupby("voting_time_group")[
            "referendum_index"
        ].count()
        second_graph_data = [
            go.Pie(
                labels=df_voting_group_sum.index,
                values=df_voting_group_sum.values,
                marker=dict(colors=voting_group_colors),
                # hovertemplate="Referendum id: %{x:.0f}<br>"
                # + "Group count: %{y:.0f}<br>"
                # + "Total: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            )
        ]
        second_graph_layout = go.Layout(
            title="<b>When Wallets Voted</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Count of voting time groups", linecolor="#021C1E"),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
            template="plotly_dark",
            hovermode="x",
        )

        fig_second_graph = go.Figure(data=second_graph_data, layout=second_graph_layout)
        return fig_second_graph
    return None


@app.callback(
    output=Output("delegate_to_chart", "figure"),
    inputs=[
        Input("specific-account-data", "data"),
        Input("delegation-data", "data"),
        Input("full-referenda-data", "data"),
    ],
)
def update_delegate_to_chart(account_data, delegation_data, referenda_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_delegation = pd.DataFrame(delegation_data)
        df_referenda = pd.DataFrame(referenda_data)
        df_delegate_to = df_delegation.merge(
            df_account, how="inner", left_on="wallet", right_on="voter"
        )
        df_delegate_to = df_delegate_to.merge(
            df_referenda, how="inner", on="referendum_index"
        )
        df_past_delegate_to = df_delegate_to[
            (
                (
                    df_delegate_to["not_passed_at"]
                    > df_delegate_to["delegation_started_at"]
                )
                & (
                    df_delegate_to["not_passed_at"]
                    < df_delegate_to["delegation_ended_at"]
                )
            )
            | (
                (df_delegate_to["passed_at"] > df_delegate_to["delegation_started_at"])
                & (df_delegate_to["passed_at"] < df_delegate_to["delegation_ended_at"])
            )
            | (df_delegate_to["delegation_ended_at"].isnull())
        ]
        df_past_delegate_to = (
            df_past_delegate_to.groupby("referendum_index")["voted_amount"]
            .sum()
            .reset_index()
        )
        df_active_delegate_to = df_delegate_to[
            (df_delegate_to["delegation_ended_at"].isnull())
        ]
        first_graph_data = [
            go.Bar(
                name="Past Delegate To",
                x=df_past_delegate_to["referendum_index"],
                y=df_past_delegate_to["voted_amount"],
                marker_color="#ffffff",
                # hovertemplate="<b>Aye Votes</b><br><br>"
                #               + "Referendum id: %{x:.1f}<br>"
                #               + "Turnout perc - aye: %{y:.1f}<br>"
                #               + "Turnout perc: %{custom
                #               data:.1f}<br>"
                #               + "<extra></extra>",
            ),
            go.Bar(
                name="Active Delegate To",
                x=df_active_delegate_to["referendum_index"],
                y=df_active_delegate_to["voted_amount"],
                marker_color="#e6007a",
                # hovertemplate="<b>Aye Votes</b><br><br>"
                #               + "Referendum id: %{x:.1f}<br>"
                #               + "Turnout perc - aye: %{y:.1f}<br>"
                #               + "Turnout perc: %{custom
                #               data:.1f}<br>"
                #               + "<extra></extra>",
            ),
        ]
        first_graph_layout = go.Layout(
            title="<b>Delegation Votes</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Voted Amount with Conviction", linecolor="#021C1E"),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
            template="plotly_dark",
            hovermode="x",
        )
        fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
        fig_first_graph.update_traces(opacity=0.75)
        return fig_first_graph
    return None


@app.callback(
    output=Output("delegated_chart", "figure"),
    inputs=[
        Input("specific-account-data", "data"),
        Input("delegation-data", "data"),
        Input("full-referenda-data", "data"),
    ],
)
def update_delegated_chart(account_data, delegation_data, referenda_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_delegation = pd.DataFrame(delegation_data)
        df_referenda = pd.DataFrame(referenda_data)
        df_delegated = df_delegation.merge(
            df_account, how="inner", left_on="delegated_to", right_on="voter"
        )
        df_delegated = df_delegated.merge(
            df_referenda, how="inner", on="referendum_index"
        )
        df_past_delegated = df_delegated[
            (
                (df_delegated["not_passed_at"] > df_delegated["delegation_started_at"])
                & (df_delegated["not_passed_at"] < df_delegated["delegation_ended_at"])
            )
            | (
                (df_delegated["passed_at"] > df_delegated["delegation_started_at"])
                & (df_delegated["passed_at"] < df_delegated["delegation_ended_at"])
            )
            | (df_delegated["delegation_ended_at"].isnull())
        ]
        df_past_delegated = (
            df_past_delegated.groupby("referendum_index")["voted_amount"]
            .sum()
            .reset_index()
        )
        df_active_delegated = df_delegated[
            (df_delegated["delegation_ended_at"].isnull())
        ]
        first_graph_data = [
            go.Bar(
                name="Past Delegated",
                x=df_past_delegated["referendum_index"],
                y=df_past_delegated["voted_amount"],
                marker_color="#ffffff",
                # hovertemplate="<b>Aye Votes</b><br><br>"
                #               + "Referendum id: %{x:.1f}<br>"
                #               + "Turnout perc - aye: %{y:.1f}<br>"
                #               + "Turnout perc: %{custom
                #               data:.1f}<br>"
                #               + "<extra></extra>",
            ),
            go.Bar(
                name="Active Delegated",
                x=df_active_delegated["referendum_index"],
                y=df_active_delegated["voted_amount"],
                marker_color="#e6007a",
                # hovertemplate="<b>Aye Votes</b><br><br>"
                #               + "Referendum id: %{x:.1f}<br>"
                #               + "Turnout perc - aye: %{y:.1f}<br>"
                #               + "Turnout perc: %{custom
                #               data:.1f}<br>"
                #               + "<extra></extra>",
            ),
        ]
        first_graph_layout = go.Layout(
            title="<b>Delegated Votes</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Voted Amount with Conviction", linecolor="#021C1E"),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
            template="plotly_dark",
            hovermode="x",
        )
        fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
        fig_first_graph.update_traces(opacity=0.75)
        return fig_first_graph
    return None


@app.callback(
    output=Output("voter-type-timeline-chart", "figure"),
    inputs=[
        Input("specific-account-data", "data"),
    ],
)
def voter_type_barchart(account_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_normal = df_account[df_account["voter_type"]=='normal']
        df_validator = df_account[df_account["voter_type"]=='validator']
        df_councillor = df_account[df_account["voter_type"]=='councillor']
        df_councillor_validator = df_account[df_account["voter_type"]=='validator + councillor']
        first_graph_data = [
            go.Scatter(
                name="Normal Votes",
                x=df_normal["referendum_index"],
                y=df_normal["voter_type"],
                marker_color="#e6007a",
            ),
            go.Scatter(
                name="Validator Votes",
                x=df_validator["referendum_index"],
                y=df_validator["voter_type"],
                marker_color="#e6007a",
            ),
            go.Scatter(
                name="Councillor Votes",
                x=df_councillor["referendum_index"],
                y=df_councillor["voter_type"],
                marker_color="#e6007a",
            ),
            go.Scatter(
                name="Councillor + Validator Votes",
                x=df_councillor_validator["referendum_index"],
                y=df_councillor_validator["voter_type"],
                marker_color="#e6007a",
            ),
        ]
        first_graph_layout = go.Layout(
            title="<b>Voter Type Timeline</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Voter Type", linecolor="#021C1E"),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
            template="plotly_dark",
            hovermode="x",
        )
        fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
        fig_first_graph.update_traces(opacity=0.75)
        return fig_first_graph
    return None



@app.callback(
    Output("quiz-correctness-table", "children"),
    inputs=[Input("specific-account-data", "data")],
)
def create_top_5_delegtation_table(account_data):
    df = pd.DataFrame(account_data)
    df = df[df["correct_answers_count"].notnull()]
    if not df.empty:
        df["quiz_correctness"] = df.apply(
            lambda row: f"{row['correct_answers_count']:.0f} / {row['questions_count']:.0f}",
            axis=1,
        )
        df = df[["referendum_index", "quiz_correctness"]]
        my_table = dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            sort_action="native",
            style_data_conditional=(
                [
                    {
                        "if": {
                            "column_id": "referendum_index",
                        },
                        "fontWeight": "bold",
                        "color": "#e6007a",
                    }
                ]
            ),
            style_cell={
                "width": "100px",
                "minWidth": "100px",
                "maxWidth": "100px",
                "overflow": "hidden",
                "textOverflow": "ellipsis",
                "fontSize": 12,
                "fontFamily": "Unbounded Blond",
            },
            style_header={"backgroundColor": "#161a28", "color": "darkgray"},
            style_data={"backgroundColor": "#161a28", "color": "white"},
            page_size=10,
              style_table={"height": "350px", "overflowY": "auto"},
        )
    else:
        my_table=None
    return my_table
