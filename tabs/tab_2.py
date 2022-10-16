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
import datetime
import plotly.express as px

subsquid_endpoint = "https://squid.subsquid.io/referenda-dashboard/v/0/graphql"


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
                            id="referendum_input_warning",
                            children=[],
                        ),
                        html.Div(
                            className="twelve columns",
                            children=[
                                html.Button(
                                    "Confirm",
                                    id="referendum-trigger-btn",
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
                ),
                html.Div(className="twelve columns", id="tab2_charts", children=[]),
                dcc.Store(
                    id="specific-referendum-data", data=[], storage_type="memory"
                ),
                dcc.Store(
                    id="specific-referenda-stats", data=[], storage_type="memory"
                ),
            ],
        )
    ]


def build_charts():
    return [
        html.Div(
            className="twelve columns gragh-block",
            children=[
                dcc.Graph(
                    id="referendum_timeline",
                    figure=blank_figure(),
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
            className="twelve columns graph-block", children=[html.P("PA Description")]
        ),
        html.Div(
            className="twelve columns",
            id="tab_2_card_row_2",
            children=[],
        ),
        html.Div(className="twelve columns", children=[html.Br()]),
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
    ]


layout = build_tab_2()

# Callback to update the referendum df
@app.callback(
    [
        Output("specific-referendum-data", "data"),
        Output("specific-referenda-stats", "data"),
        Output("referendum_input_warning", "children"),
    ],
    [
        Input("full-referenda-data", "data"),
        Input("referendum-trigger-btn", "n_clicks"),
        Input("referendum_input", "value"),
    ],
)
def update_specific_referendum_data(referenda_data, n_clicks, referendum_input):
    warning = None
    df_specific_referendum = pd.DataFrame()
    df_referenda = pd.DataFrame(referenda_data)
    df_specific_referenda_stats = pd.DataFrame()
    if referendum_input:
        try:
            df_specific_referendum = load_specific_referendum_stats(referendum_input)
            df_specific_referenda_stats = df_referenda[
                df_referenda["referendum_index"] == int(referendum_input)
            ]
        except:
            warning = html.P(className="alert alert-danger", children=["Invalid input"])
        if df_specific_referendum.empty:
            warning = html.P(className="alert alert-danger", children=["Invalid input"])
        return (
            df_specific_referendum.to_dict("record"),
            df_specific_referenda_stats.to_dict("record"),
            [warning],
        )
    return None, None, html.P()


@app.callback(
    output=Output("tab2_charts", "children"),
    inputs=[
        Input("referendum-trigger-btn", "n_clicks"),
        Input("referendum_input_warning", "children"),
    ],
)
def build_tab2_charts(n_clicks, input_warning):
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
                className="four columns graph-block",
                id="card1",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4("Section", className="card-title"),
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
                className="four columns graph-block",
                id="card2",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4("Method", className="card-title"),
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
                className="four columns graph-block",
                id="card3",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4("Proposer", className="card-title"),
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
                                    html.H4("Vote Total", className="card-title"),
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
                                    html.H4("Voted Amount", className="card-title"),
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
                                    html.H4("Turnout (%)", className="card-title"),
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
                                    html.H4("New Accounts", className="card-title"),
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
    output=Output("cum_voted_amount_chart", "figure"),
    inputs=[Input("specific-referendum-data", "data")],
)
def cum_voted_amount_chart(referendum_data):
    if referendum_data:
        df_referenda = pd.DataFrame(referendum_data)
        second_graph_data = [
            go.Scatter(
                name="Aye Votes",
                x=df_referenda["timestamp"],
                y=df_referenda["cum_voted_amount_with_conviction_aye"],
                mode="lines",
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
def cum_voted_amount_chart(referendum_data):
    if referendum_data:
        df_referenda = pd.DataFrame(referendum_data)
        df_aye = df_referenda[df_referenda["decision"] == "aye"]
        df_nay = df_referenda[df_referenda["decision"] == "nay"]
        third_graph_data = [
            go.Box(
                name="Aye Votes",
                x=df_aye["voted_amount_with_conviction"],
                boxpoints=False,
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
