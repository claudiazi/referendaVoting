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


import plotly.express as px

subsquid_endpoint = "https://squid.subsquid.io/referenda-dashboard/v/1/graphql"


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
    df_account = pd.DataFrame.from_dict(account_data["data"]["accountStats"])
    df_account = df_account.sort_values("referendum_index")
    print(f"finish loading account_stats {time.time() - start_time}")
    return df_account


def build_tab_3():
    return [
        html.Div(
            className="section-banner",
            children=[
                html.Div(
                    className="twelve columns",
                    children=[
                        html.P(
                            "Type in the Address: ",
                            style={"display": "inline-block"},
                        ),
                        dcc.Input(id="account_input", placeholder="number"),
                    ],
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
                            id="referendum-trigger-btn",
                            n_clicks=0,
                            style={"display": "inline-block", "float": "middle"},
                        )
                    ],
                ),
                html.Div(className="twelve columns", id="tab3_charts", children=[]),
                dcc.Store(id="specific-account-data", data=[], storage_type="memory"),
            ],
        )
    ]


def build_charts():
    return [
        html.Div(
            className="twelve columns",
            id="tab3_card_row_1",
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
    ]


layout = build_tab_3()

# Callback to update the referendum df
@app.callback(
    [
        Output("specific-account-data", "data"),
        Output("account_input_warning", "children"),
    ],
    [
        Input("referendum-trigger-btn", "n_clicks"),
        Input("account_input", "value"),
    ],
)
def update_specific_account_data(n_clicks, account_input):
    warning = None
    df_specific_account = pd.DataFrame()
    if account_input:
        try:
            df_specific_account = load_specific_account_stats(account_input)
        except:
            warning = html.P(className="alert alert-danger", children=["Invalid input"])
        if df_specific_account.empty:
            warning = html.P(className="alert alert-danger", children=["Invalid input"])
        return (
            df_specific_account.to_dict("record"),
            [warning],
        )
    return None, html.P()


@app.callback(
    output=Output("tab3_charts", "children"),
    inputs=[
        Input("referendum-trigger-btn", "n_clicks"),
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
            barmode="overlay",
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
