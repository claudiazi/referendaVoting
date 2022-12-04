import datetime
import json
import time

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import requests
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from utils.plotting import blank_figure

subsquid_endpoint = "https://squid.subsquid.io/referenda-dashboard/v/0/graphql"

polkassembly_graphql_endpoint = "https://kusama.polkassembly.io/v1/graphql"


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


def build_tab_2():
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
                                    id="referendum_input",
                                    placeholder="Type in Referendum Index",
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
                            id="input_check",
                            children=[
                                dcc.Loading(
                                    id="referendum_input_warning",
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="twelve columns",
                    children=[dcc.Loading(id="tab2_charts", children=[])],
                ),
                dcc.Store(
                    id="specific-referendum-data",
                    data=[],
                    storage_type="memory",
                ),
                dcc.Store(
                    id="specific-referenda-stats",
                    data=[],
                    storage_type="memory",
                ),
                dcc.Store(id="specific-referendum-pa", data=[], storage_type="memory"),
                dcc.Store(
                    id="specific-referendum-votes",
                    data=[],
                    storage_type="memory",
                ),
            ],
        )
    ]


def build_charts():
    return [
        dcc.Loading(
            id="loading-icon",
            children=[
                html.Div(
                    className="twelve columns gragh-block",
                    children=[
                        dcc.Loading(
                            dcc.Graph(
                                id="referendum_timeline",
                                figure=blank_figure(),
                            )
                        )
                    ],
                ),
                html.Div(
                    className="twelve columns",
                    id="tab_2_card_row_1",
                    children=[],
                ),
                html.Div(className="twelve columns", children=[html.Br()]),
                html.Div(
                    className="twelve columns graph-block",
                    children=[],
                    id="pa-description",
                ),
                html.Div(className="twelve columns", children=[html.Br()]),
                html.Div(
                    className="twelve columns",
                    id="tab_2_card_row_2",
                    children=[],
                ),
                html.Div(className="twelve columns", children=[html.Br()]),
                html.Div(
                    className="twelve columns",
                    children=[
                        html.Div(
                            className="four columns graph-block",
                            children=[
                                html.Div(
                                    id="iii-chart",
                                    className="twelve columns",
                                    children=[
                                        dcc.Loading(
                                            id="loading-icon",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="aye_nay_chart",
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
                        html.Div(
                            className="four columns graph-block",
                            children=[
                                html.Div(
                                    className="twelve columns",
                                    children=[
                                        dcc.Loading(
                                            id="loading-icon",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="delegation_chart",
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
                        html.Div(
                            className="four columns graph-block",
                            children=[
                                html.Div(
                                    className="twelve columns",
                                    children=[
                                        dcc.Loading(
                                            id="loading-icon",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="voter_type_chart",
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
                                        dcc.Loading(
                                            id="loading-icon",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="cum_voted_amount_chart",
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
                                                        id="distribution_voted_amount_scatterchart",
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
                html.Div(className="twelve columns", children=[html.Br()]),
                html.Div(
                    className="section-banner", children="Top 5 Delegated Accounts"
                ),
                html.Div(className="twelve columns", children=[html.Br()]),
                html.Div(
                    className="twelve columns",
                    children=[
                        dcc.Loading(
                            html.Div(
                                id="top-5-delegated-table",
                                children=[],
                            )
                        )
                    ],
                ),
                html.Div(className="twelve columns", children=[html.Br()]),
            ],
        )
    ]


layout = build_tab_2()


@app.callback(
    [
        Output("specific-referendum-data", "data"),
        Output("specific-referenda-stats", "data"),
        Output("specific-referendum-pa", "data"),
        Output("specific-referendum-votes", "data"),
        Output("referendum_input_warning", "children"),
    ],
    [
        Input("full-referenda-data", "data"),
        Input("referendum_input", "value"),
    ],
)
def update_specific_referendum_data(referenda_data, referendum_input):
    warning = None
    df_specific_referendum = pd.DataFrame()
    df_referenda = pd.DataFrame(referenda_data)
    df_specific_referenda_stats = pd.DataFrame()
    df_specific_referendum_pa = pd.DataFrame()
    df_referendum_votes = pd.DataFrame()
    if referendum_input:
        try:
            df_specific_referendum = load_specific_referendum_stats(referendum_input)
            df_specific_referenda_stats = df_referenda[
                df_referenda["referendum_index"] == int(referendum_input)
            ]
            df_specific_referendum_pa = load_pa_description(referendum_input)
            df_referendum_votes = load_refereundum_votes(referendum_input)
        except:
            warning = dcc.Loading(
                id="loading-icon",
                children=[
                    html.P(className="alert alert-danger", children=["Invalid input"])
                ],
            )
        if df_specific_referendum.empty:
            warning = html.P(className="alert alert-danger", children=["Invalid input"])
        return (
            df_specific_referendum.to_dict("record"),
            df_specific_referenda_stats.to_dict("record"),
            df_specific_referendum_pa.to_dict("record"),
            df_referendum_votes.to_dict("record"),
            [warning],
        )
    return None, None, None, None, html.P()


@app.callback(
    output=Output("tab2_charts", "children"),
    inputs=[
        Input("referendum_input_warning", "children"),
    ],
)
def build_tab2_charts(input_warning):
    if input_warning == [None]:
        return build_charts()


# Update tenth chart
@app.callback(
    output=Output("referendum_timeline", "figure"),
    inputs=[
        Input("specific-referenda-stats", "data"),
        Input("tab2_charts", "children"),
    ],
)
def update_timeline(referenda_data, children_content):
    fig_first_graph = None
    if referenda_data:
        df_referenda = pd.DataFrame(referenda_data)
        print(df_referenda.columns)
        df_timeline = df_referenda[
            [
                "referendum_index",
                "created_at",
                "cancelled_at",
                "executed_at",
                "passed_at",
                "not_passed_at",
                "ends_at",
                "executes_at",
            ]
        ]
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        df_timeline["now"] = now
        df_timeline["now"] = df_timeline.apply(
            lambda row: row["now"]
            if (
                not row["executed_at"]
                and not row["passed_at"]
                and not row["not_passed_at"]
                and not row["cancelled_at"]
            )
            else None,
            axis=1,
        )
        timeline_colors = {
            "created_at": "#e1f5c4",
            "cancelled_at": "#ede574",
            "executed_at": "#f9d423",
            "passed_at": "#fc913a",
            "not_passed_at": "#ff4e50",
            "now": "#00d7ff",
            "ends_at": "#fc913a",
            "executes_at": "#f9d423",
        }
        df_timeline = df_timeline.set_index(("referendum_index"))
        df_timeline = df_timeline.stack().reset_index()
        df_timeline.columns = ["referendum_index", "timeline", "timestamp"]
        df_timeline["y"] = 0
        first_graph_data = []
        for timeline in [
            "created_at",
            "cancelled_at",
            "executed_at",
            "passed_at",
            "not_passed_at",
            "now",
            "executes_at",
            "ends_at",
        ]:
            df = df_timeline[df_timeline["timeline"] == timeline]
            first_graph_data.append(
                go.Scatter(
                    x=df["timestamp"],
                    y=df["y"],
                    name=timeline,
                    marker=dict(size=20, color=timeline_colors[timeline]),
                    customdata=df["timeline"],
                    hovertemplate="<b>%{customdata}</b><br><br>"
                    + "Timestamp: %{x}<br>"
                    + "<extra></extra>",
                ),
            )
        first_graph_layout = go.Layout(
            title="<b>Timeline</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            template="plotly_dark",
            hovermode="x",
            autosize=True,
            yaxis_visible=False,
            yaxis_showticklabels=False,
            height=200,
        )
        fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
        if "now" in df_timeline["timeline"].to_list():
            fig_first_graph.add_shape(
                type="line",
                x0=now,
                y0=0,
                x1=df_timeline["timestamp"].max(),
                y1=0,
                line=dict(
                    color="#ffb3e0",
                    width=4,
                    dash="dot",
                ),
            )
            fig_first_graph.add_shape(
                type="line",
                x0=df_timeline["timestamp"].min(),
                y0=0,
                x1=now,
                y1=0,
                line=dict(
                    color="#e6007a",
                    width=4,
                    dash="dot",
                ),
            )
        else:
            fig_first_graph.add_shape(
                type="line",
                x0=df_timeline["timestamp"].min(),
                y0=0,
                x1=df_timeline["timestamp"].max(),
                y1=0,
                line=dict(
                    color="#e6007a",
                    width=4,
                    dash="dot",
                ),
            )
        fig_first_graph.update_layout(
            yaxis_range=[
                df_timeline["timestamp"].min(),
                df_timeline["timestamp"].max(),
            ],
        )
    return fig_first_graph


@app.callback(
    output=Output("tab_2_card_row_1", "children"),
    inputs=[
        Input("specific-referenda-stats", "data"),
    ],
)
def update_card1(referenda_data):
    if referenda_data:
        df_referenda = pd.DataFrame(referenda_data)
        return [
            html.Div(
                className="three columns graph-block",
                id="card1",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Section", className="card-title"),
                                    html.P(
                                        df_referenda["section"],
                                        className="card-value",
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
            ),
            html.Div(
                className="three columns graph-block",
                id="card2",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Method", className="card-title"),
                                    html.P(
                                        df_referenda["method"],
                                        className="card-value",
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
            ),
            html.Div(
                className="three columns graph-block",
                id="card2",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Passing Threshold", className="card-title"
                                    ),
                                    html.P(
                                        df_referenda["threshold_type"],
                                        className="card-value",
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
            ),
            html.Div(
                className="three columns graph-block",
                id="card3",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Proposer", className="card-title"),
                                    html.P(
                                        df_referenda["proposer"],
                                        className="card-value",
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
            ),
        ]

    return None


@app.callback(
    output=Output("tab_2_card_row_2", "children"),
    inputs=[
        Input("specific-referenda-stats", "data"),
    ],
)
def update_card2(referenda_data):
    if referenda_data:
        df_referenda = pd.DataFrame(referenda_data)
        return [
            html.Div(
                className="three columns graph-block",
                id="card4",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Vote Total", className="card-title"),
                                    html.P(
                                        f"{df_referenda['count_total'].values[0]}",
                                        className="card-value",
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
            ),
            html.Div(
                className="three columns graph-block",
                id="card2",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Voted Amount", className="card-title"),
                                    html.P(
                                        f"{df_referenda['voted_amount_total'].values[0]:.2f} KSM",
                                        className="card-value",
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
            ),
            html.Div(
                className="three columns graph-block",
                id="card2",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Turnout (%)", className="card-title"),
                                    html.P(
                                        f"{df_referenda['turnout_total_perc'].values[0]:.2f}",
                                        className="card-value",
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
            ),
            html.Div(
                className="three columns graph-block",
                id="card3",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("New Accounts", className="card-title"),
                                    html.P(
                                        f"{df_referenda['count_new'].values[0]}",
                                        f"{df_referenda['count_new_perc'].values[0]}",
                                        className="card-value",
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
            ),
        ]

    return None


@app.callback(
    output=Output("pa-description", "children"),
    inputs=[
        Input("specific-referendum-pa", "data"),
    ],
)
def update_pa_description(referendum_pa_data):
    if referendum_pa_data:
        df_referendum_pa = pd.DataFrame(referendum_pa_data)
        return [
            dbc.Card(
                className="twelve columns",
                children=[
                    dbc.CardBody(
                        [
                            html.H5("PA Description", className="card-title"),
                            html.Strong(
                                df_referendum_pa["title"].values[0],
                                className="card-text",
                            ),
                        ]
                    ),
                ],
            ),
            html.Div(
                [
                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Markdown(df_referendum_pa["content"].values[0]),
                                className="small_card_body",
                            )
                        ),
                        id="collapse",
                        is_open=False,
                    ),
                    dbc.Button(
                        "Read more",
                        id="collapse-button",
                        className="mb-3 click-button",
                        n_clicks=0,
                    ),
                ]
            ),
        ]

    return None


@app.callback(
    output=Output("collapse", "is_open"),
    inputs=[Input("collapse-button", "n_clicks"), Input("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    output=Output("cum_voted_amount_chart", "figure"),
    inputs=[Input("specific-referendum-votes", "data")],
)
def cum_voted_amount_chart(votes_data):
    if votes_data:
        df_referenda = pd.DataFrame(votes_data)
        second_graph_data = [
            go.Scatter(
                name="Aye Votes",
                x=df_referenda["timestamp"],
                y=df_referenda["cum_voted_amount_with_conviction_aye"],
                mode="lines",
                marker_color="#ffffff",
                # hovertemplate="<b>Aye Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Aye amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
            go.Scatter(
                name="Nay Votes",
                x=df_referenda["timestamp"],
                y=df_referenda["cum_voted_amount_with_conviction_nay"],
                mode="lines",
                marker_color="#e6007a",
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
    output=Output("distribution_voted_amount_scatterchart", "figure"),
    inputs=[Input("specific-referendum-data", "data")],
)
def voted_amount_distribution_chart(referendum_data):
    if referendum_data:
        df_referenda = pd.DataFrame(referendum_data)
        df_aye = df_referenda[df_referenda["decision"] == "aye"]
        df_nay = df_referenda[df_referenda["decision"] == "nay"]
        third_graph_data = [
            go.Box(
                name="Aye Votes",
                x=df_aye["voted_amount_with_conviction"],
                boxpoints=False,
                marker_color="#ffffff",
                # hovertemplate="<b>Aye Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Aye amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
            go.Box(
                name="Nay Votes",
                x=df_nay["voted_amount_with_conviction"],
                boxpoints=False,
                marker_color="#e6007a",
                # hovertemplate="<b>Nay Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Nay Amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
        ]

        third_graph_layout = go.Layout(
            title="<b>Voted Amount Distribution</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="overlay",
            xaxis=dict(title="Voted Amount with Conviction (KSM)", linecolor="#BCCCDC"),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
            template="plotly_dark",
            hovermode="y",
        )
        fig_thrid_graph = go.Figure(data=third_graph_data, layout=third_graph_layout)
        fig_thrid_graph.update_traces(opacity=0.75)
        return fig_thrid_graph
    return None


@app.callback(
    output=Output("aye_nay_chart", "figure"),
    inputs=[Input("specific-referenda-stats", "data")],
)
def aye_nay_chart(referendum_data):
    if referendum_data:
        df_referenda = pd.DataFrame(referendum_data)
        df_referenda["voted_amount_aye_perc"] = round(
            df_referenda["voted_amount_aye"] / df_referenda["voted_amount_total"] * 100,
            2,
        )
        df_referenda["voted_amount_nay_perc"] = round(
            df_referenda["voted_amount_nay"] / df_referenda["voted_amount_total"] * 100,
            2,
        )
        third_graph_data = [
            go.Bar(
                name="Aye Votes",
                x=df_referenda["voted_amount_aye_perc"],
                y=["referendum_index"],
                textposition="auto",
                orientation="h",
                marker_color="#ffffff",
                texttemplate="<b>%{x} %</b>",
                # hovertemplate="<b>Aye Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Aye amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
            go.Bar(
                name="Aye Votes",
                x=df_referenda["voted_amount_nay_perc"],
                y=["referendum_index"],
                textposition="auto",
                orientation="h",
                marker_color="#e6007a",
                texttemplate="<b>%{x} %</b>",
                textangle=0,
                textfont_color="white",
                # hovertemplate="<b>Aye Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Aye amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
        ]
        annotations = []
        space = 0
        for x, category in zip(
            [
                df_referenda["voted_amount_aye_perc"].values[0],
                df_referenda["voted_amount_nay_perc"].values[0],
            ],
            ["Aye", "Nay"],
        ):
            annotations.append(
                dict(
                    xref="x",
                    yref="paper",
                    x=space + x / 2,
                    y=-0.2,
                    xanchor="center",
                    text=f"{category}",
                    showarrow=False,
                    align="right",
                )
            )
            space += x

        third_graph_layout = go.Layout(
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
            ),
            template="plotly_dark",
            hovermode="y",
            showlegend=False,
            height=120,
            margin=dict(l=0, r=0, t=20, b=30, pad=4),
        )
        fig_thrid_graph = go.Figure(data=third_graph_data, layout=third_graph_layout)
        fig_thrid_graph.update_traces(opacity=0.75)
        fig_thrid_graph.update_layout(annotations=annotations)
        return fig_thrid_graph
    return None


@app.callback(
    output=Output("delegation_chart", "figure"),
    inputs=[Input("specific-referenda-stats", "data")],
)
def aye_nay_chart(referendum_data):
    if referendum_data:
        df_referenda = pd.DataFrame(referendum_data)
        df_referenda["voted_amount_direct_perc"] = round(
            df_referenda["voted_amount_direct"]
            / (
                df_referenda["voted_amount_delegated"]
                + df_referenda["voted_amount_direct"]
            )
            * 100,
            2,
        )
        df_referenda["voted_amount_delegated_perc"] = round(
            df_referenda["voted_amount_delegated"]
            / (
                df_referenda["voted_amount_delegated"]
                + df_referenda["voted_amount_direct"]
            )
            * 100,
            2,
        )
        third_graph_data = [
            go.Bar(
                name="Direct Votes",
                x=df_referenda["voted_amount_direct_perc"],
                y=["referendum_index"],
                textposition="inside",
                orientation="h",
                marker_color="#ffffff",
                texttemplate="<b>%{x} %</b>",
                # hovertemplate="<b>Aye Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Aye amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
            go.Bar(
                name="Delegated Votes",
                x=df_referenda["voted_amount_delegated_perc"],
                y=["referendum_index"],
                textposition="inside",
                orientation="h",
                marker_color="#e6007a",
                texttemplate="<b>%{x} %</b>",
                textangle=0,
                # hovertemplate="<b>Aye Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Aye amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
        ]
        annotations = []
        space = 0
        for x, category in zip(
            [
                df_referenda["voted_amount_direct_perc"].values[0],
                df_referenda["voted_amount_delegated_perc"].values[0],
            ],
            ["Direct", "Delegated"],
        ):
            annotations.append(
                dict(
                    xref="x",
                    yref="paper",
                    x=space + x / 2,
                    y=-0.2,
                    xanchor="center",
                    text=f"{category}",
                    showarrow=False,
                    align="right",
                )
            )
            space += x

        third_graph_layout = go.Layout(
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
            ),
            template="plotly_dark",
            hovermode="y",
            showlegend=False,
            height=120,
            margin=dict(l=0, r=0, t=20, b=30, pad=4),
        )
        fig_thrid_graph = go.Figure(data=third_graph_data, layout=third_graph_layout)
        fig_thrid_graph.update_traces(opacity=0.75)
        fig_thrid_graph.update_layout(annotations=annotations)
        return fig_thrid_graph
    return None


@app.callback(
    output=Output("voter_type_chart", "figure"),
    inputs=[Input("specific-referenda-stats", "data")],
)
def aye_nay_chart(referendum_data):
    if referendum_data:
        df_referenda = pd.DataFrame(referendum_data)
        df_referenda["voted_amount_validator_perc"] = round(
            df_referenda["voted_amount_validator"]
            / (
                df_referenda["voted_amount_validator"]
                + df_referenda["voted_amount_normal"]
                + df_referenda["voted_amount_councillor"]
            )
            * 100,
            2,
        )
        df_referenda["voted_amount_normal_perc"] = round(
            df_referenda["voted_amount_normal"]
            / (
                df_referenda["voted_amount_validator"]
                + df_referenda["voted_amount_normal"]
                + df_referenda["voted_amount_councillor"]
            )
            * 100,
            2,
        )
        df_referenda["voted_amount_councillor_perc"] = round(
            df_referenda["voted_amount_councillor"]
            / (
                df_referenda["voted_amount_validator"]
                + df_referenda["voted_amount_normal"]
                + df_referenda["voted_amount_councillor"]
            )
            * 100,
            2,
        )
        third_graph_data = [
            go.Bar(
                name="Validator Votes",
                x=df_referenda["voted_amount_validator_perc"],
                y=["referendum_index"],
                textposition="inside",
                orientation="h",
                marker_color="#e6007a",
                texttemplate="<b>%{x} %</b>",
                # hovertemplate="<b>Aye Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Aye amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
            go.Bar(
                name="Normal Votes",
                x=df_referenda["voted_amount_normal_perc"],
                y=["referendum_index"],
                textposition="inside",
                orientation="h",
                marker_color="#ffffff",
                texttemplate="<b>%{x} %</b>",
                textangle=0,
                # hovertemplate="<b>Aye Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Aye amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
            go.Bar(
                name="Councillor Votes",
                x=df_referenda["voted_amount_councillor_perc"],
                y=["referendum_index"],
                textposition="inside",
                orientation="h",
                marker_color="#ffb3e0",
                texttemplate="<b>%{x} %</b>",
                textangle=0,
                # hovertemplate="<b>Aye Votes</b><br><br>"
                # + "Referendum id: %{x:.0f}<br>"
                # + "Aye amount: %{y:.0f}<br>"
                # + "Turnout: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
        ]
        annotations = []
        space = 0
        for x, category in zip(
            [
                df_referenda["voted_amount_validator_perc"].values[0],
                df_referenda["voted_amount_normal_perc"].values[0],
                df_referenda["voted_amount_councillor_perc"].values[0],
            ],
            ["Validator", "Normal", "Councillor"],
        ):
            annotations.append(
                dict(
                    xref="x",
                    yref="paper",
                    x=space + x / 2,
                    y=-0.2,
                    xanchor="center",
                    text=f"{category}",
                    showarrow=False,
                    align="right",
                )
            )
            space += x

        third_graph_layout = go.Layout(
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
            ),
            template="plotly_dark",
            hovermode="y",
            showlegend=False,
            height=120,
            margin=dict(l=0, r=0, t=20, b=30, pad=4),
        )
        fig_thrid_graph = go.Figure(data=third_graph_data, layout=third_graph_layout)
        fig_thrid_graph.update_traces(opacity=0.75)
        fig_thrid_graph.update_layout(annotations=annotations)
        return fig_thrid_graph
    return None


@app.callback(
    Output("top-5-delegated-table", "children"),
    inputs=[Input("specific-referendum-data", "data")],
)
def create_top_5_delegtation_table(referendum_data_data):
    df = pd.DataFrame(referendum_data_data)
    df = (
        df.groupby("delegated_to")["voted_amount_with_conviction"]
        .sum()
        .sort_values(ascending=False)
        .head()
        .reset_index()
    )
    df["voted_amount_with_conviction"] = df["voted_amount_with_conviction"].apply(
        lambda x: round(x, 2)
    )
    my_table = dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        sort_action="native",
        style_data_conditional=(
            [
                {
                    "if": {
                        "column_id": "delegated_to",
                    },
                    "fontWeight": "bold",
                    "color": "#e6007a",
                }
            ]
            # + data_perc_bars(dff, "voted_amount_aye")
            # + data_perc_bars(dff, "voted_amount_nay")
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
        #   style_table={"height": "200px", "overflowY": "auto"},
        #    css=[
        #        {"selector": ".dash-spreadsheet tr th", "rule": "height: 30px;"},
        #        # set height of header
        #        {"selector": ".dash-spreadsheet tr td", "rule": "height: 25px;"},
        #        # set height of body rows
        #    ]
    )
    return my_table


# Update x chart
# @app.callback(
#     Output("quiz_correctness_piechart", "figure"),
#     [
#         Input("specific-referenda-stats", "data"),
#     ],
# )
# def update_pie_chart(
#     referenda_data
# ):
#     df_referenda = pd.DataFrame(referenda_data)
#     df_referenda['count_1_question_correct_perc'] = df_referenda['count_1_question_correct_perc'] /
#     x_graph_data = [
#         go.Pie(
#             labels=df_method_group_count.index,
#             values=df_method_group_count.values,
#             marker=dict(colors=color_scale),
#             textposition="inside",
#             opacity=0.8,
#             # hovertemplate="Referendum id: %{x:.0f}<br>"
#             # + "Group count: %{y:.0f}<br>"
#             # + "Total: %{customdata:.0f}<br>"
#             # + "<extra></extra>",
#         )
#     ]
#     x_graph_layout = go.Layout(
#         title="<b>Method</b>",
#         paper_bgcolor="#161a28",
#         plot_bgcolor="#161a28",
#         legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
#         template="plotly_dark",
#         hovermode="x",
#         autosize=True,
#         clickmode="event+select",
#     )
#     fig_x_graph = go.Figure(data=x_graph_data, layout=x_graph_layout)
#     return fig_x_graph
