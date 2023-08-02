import datetime

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from utils.data_preparation import (
    load_refereundum_votes_gov2,
    load_specific_referendum_stats_gov2,
    load_pa_description,
)
from utils.plotting import blank_figure


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
                                    id="referendum_input_gov2",
                                    placeholder="Type in Referendum Index",
                                    style={
                                        "width": "70%",
                                        "float": "middle",
                                        "color": "black"
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
                                    id="referendum_input_warning_gov2",
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="twelve columns",
                    children=[dcc.Loading(id="tab2_charts_gov2", children=[])],
                ),
                dcc.Store(
                    id="specific-referendum-data-gov2",
                    data=[],
                    storage_type="memory",
                ),
                dcc.Store(
                    id="specific-referenda-stats-gov2",
                    data=[],
                    storage_type="memory",
                ),
                dcc.Store(
                    id="specific-referendum-pa-gov2", data=[], storage_type="memory"
                ),
                dcc.Store(
                    id="specific-referendum-votes-gov2",
                    data=[],
                    storage_type="memory",
                ),
                html.Footer(
                    className="logo-footer twelve columns",
                    children=[
                        html.Footer(
                            className="logo-footer-centering",
                            children=[
                                html.A(
                                    href="https://www.proofofchaos.app/",
                                    target="_blank",
                                    className="logo-footer-container",
                                    children=[
                                        html.H4(
                                            children=["Built by "],
                                            className="footer-element",
                                        ),
                                        html.Img(
                                            src="assets/proofofchaos_white.png",
                                            id="proofofchaos-icon",
                                            className="footer-element",
                                        ),
                                    ],
                                ),
                                html.A(
                                    href="https://kusama.polkassembly.io/treasury-proposals",
                                    target="_blank",
                                    className="logo-footer-container",
                                    children=[
                                        html.H4(
                                            children=["Funded by "],
                                            className="footer-element",
                                        ),
                                        html.Img(
                                            src="assets/kusama.png",
                                            id="kusama-icon",
                                            className="footer-element",
                                        ),
                                    ],
                                ),
                                html.A(
                                    href="https://subsquid.io/",
                                    target="_blank",
                                    className="logo-footer-container",
                                    children=[
                                        html.H4(
                                            children=["Powered by"],
                                            className="footer-element",
                                        ),
                                        html.Img(
                                            src="assets/subsquid.png",
                                            id="subsquid-icon",
                                            className="footer-element",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    ]


def build_charts_gov2():
    return [
        dcc.Loading(
            id="loading-icon",
            children=[
                html.Div(
                    className="twelve columns gragh-block",
                    children=[
                        dcc.Loading(
                            dcc.Graph(
                                id="referendum_timeline_gov2",
                                figure=blank_figure(),
                            )
                        )
                    ],
                ),
                html.Div(
                    className="twelve columns",
                    id="tab_2_card_row_1_gov2",
                    children=[],
                ),
                html.Div(className="twelve columns", children=[html.Br()]),
                html.Div(
                    className="twelve columns graph-block",
                    children=[],
                    id="pa-description-gov2",
                ),
                html.Div(className="twelve columns", children=[html.Br()]),
                html.Div(
                    className="twelve columns",
                    id="tab_2_card_row_2_gov2",
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
                                    id="iii-chart-gov2",
                                    className="twelve columns",
                                    children=[
                                        dcc.Loading(
                                            id="loading-icon",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="aye_nay_chart_gov2",
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
                                                        id="delegation_chart_gov2",
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
                                                        id="voter_type_chart_gov2",
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
                                    id="first-chart-gov2",
                                    className="twelve columns",
                                    children=[
                                        dcc.Loading(
                                            id="loading-icon",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="cum_voted_amount_chart_gov2",
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
                                                        id="distribution_voted_amount_scatterchart_gov2",
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
                                id="top-5-delegated-table-gov2",
                                children=[],
                            )
                        )
                    ],
                ),
                html.Div(className="twelve columns", children=[html.Br()]),
                html.Div(className="section-banner", children="Top 5 Direct Voters"),
                html.Div(
                    className="twelve columns",
                    children=[
                        dcc.Loading(
                            html.Div(
                                id="top-5-direct-voter-table-gov2",
                                children=[],
                            )
                        )
                    ],
                ),
                html.Div(className="twelve columns", children=[html.Br()]),
            ],
        ),
    ]


layout = build_tab_2()


@app.callback(
    [
        Output("specific-referendum-data-gov2", "data"),
        Output("specific-referenda-stats-gov2", "data"),
        Output("specific-referendum-pa-gov2", "data"),
        Output("specific-referendum-votes-gov2", "data"),
        Output("referendum_input_warning_gov2", "children"),
    ],
    [
        Input("full-referenda-data", "data"),
        Input("referendum_input_gov2", "value"),
    ],
)
def update_specific_referendum_data(referenda_data, referendum_input_gov2):
    warning = None
    df_specific_referendum = pd.DataFrame()
    df_referenda = pd.DataFrame(referenda_data)
    df_specific_referenda_stats = pd.DataFrame()
    df_specific_referendum_pa = pd.DataFrame()
    df_referendum_votes = pd.DataFrame()
    if referendum_input_gov2:
        try:
            df_specific_referendum = load_specific_referendum_stats_gov2(
                referendum_input_gov2
            )
            df_specific_referenda_stats = df_referenda[
                df_referenda["referendum_index"] == int(referendum_input_gov2)
            ]
            # df_specific_referendum_pa = load_pa_description(referendum_input_gov2)
            df_specific_referendum_pa = load_pa_description(referendum_input_gov2)
            df_referendum_votes = load_refereundum_votes_gov2(referendum_input_gov2)
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
            df_specific_referendum.to_dict("records"),
            df_specific_referenda_stats.to_dict("records"),
            df_specific_referendum_pa.to_dict("records"),
            df_referendum_votes.to_dict("records"),
            [warning],
        )
    return None, None, None, None, html.P()


@app.callback(
    output=Output("tab2_charts_gov2", "children"),
    inputs=[
        Input("referendum_input_warning_gov2", "children"),
    ],
)
def build_tab2_charts_gov2(input_warning):
    if input_warning == [None]:
        return build_charts_gov2()


@app.callback(
    output=Output("referendum_timeline_gov2", "figure"),
    inputs=[
        Input("specific-referenda-stats-gov2", "data"),
    ],
)
def update_timeline(referenda_data):
    fig_first_graph = None
    if referenda_data:
        df_referenda = pd.DataFrame(referenda_data)
        df_timeline = df_referenda[
            [
                "referendum_index",
                "created_at",
                "cancelled_at",
                "passed_at",
                "not_passed_at",
            ]
        ]
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        df_timeline["now"] = now
        df_timeline["now"] = df_timeline.apply(
            lambda row: row["now"]
            if (
                not row["passed_at"]
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
            "passed_at",
            "not_passed_at",
            "now",
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
    output=Output("tab_2_card_row_1_gov2", "children"),
    inputs=[
        Input("specific-referenda-stats-gov2", "data"),
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
                                        "Submission Deposit Who", className="card-title"
                                    ),
                                    html.P(
                                        df_referenda["submission_deposit_who"],
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
                                    html.H5(
                                        "Decision Deposit Who", className="card-title"
                                    ),
                                    html.P(
                                        df_referenda["decision_deposit_who"],
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
    output=Output("tab_2_card_row_2_gov2", "children"),
    inputs=[
        Input("specific-referenda-stats-gov2", "data"),
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
    output=Output("pa-description-gov2", "children"),
    inputs=[
        Input("specific-referendum-pa-gov2", "data"),
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
                        id="collapse-gov2",
                        is_open=False,
                    ),
                    dbc.Button(
                        children="Read more",
                        id="collapse-gov2-button-gov2",
                        className="mb-3 click-button",
                        n_clicks=0,
                    ),
                ]
            ),
        ]

    return None


@app.callback(
    output=[
        Output("collapse-gov2", "is_open"),
        Output("collapse-gov2-button-gov2", "children"),
    ],
    inputs=[Input("collapse-gov2-button-gov2", "n_clicks")],
)
def toggle_collapse_gov2(n):
    if n % 2 == 0:
        return False, "Read more"
    return True, "Read less"


@app.callback(
    output=Output("cum_voted_amount_chart_gov2", "figure"),
    inputs=[Input("specific-referendum-votes-gov2", "data")],
)
def cum_voted_amount_chart_gov2(votes_data):
    if votes_data:
        df_referenda = pd.DataFrame(votes_data)
        second_graph_data = [
            go.Scatter(
                name="Aye Votes",
                x=df_referenda["timestamp"],
                y=df_referenda["cum_voted_amount_with_conviction_aye"],
                mode="lines",
                marker_color="#ffffff",
            ),
            go.Scatter(
                name="Nay Votes",
                x=df_referenda["timestamp"],
                y=df_referenda["cum_voted_amount_with_conviction_nay"],
                mode="lines",
                marker_color="#e6007a",
            ),
        ]

        second_graph_layout = go.Layout(
            title="<b>Cumulated Voted Amount</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Timestamp", linecolor="#BCCCDC"),
            yaxis=dict(title="Voted Amount with Conviction", linecolor="#021C1E"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
            template="plotly_dark",
            hovermode="x",
        )
        fig_second_graph = go.Figure(data=second_graph_data, layout=second_graph_layout)
        return fig_second_graph
    return None


@app.callback(
    output=Output("distribution_voted_amount_scatterchart_gov2", "figure"),
    inputs=[Input("specific-referendum-data-gov2", "data")],
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
            ),
            go.Box(
                name="Nay Votes",
                x=df_nay["voted_amount_with_conviction"],
                boxpoints=False,
                marker_color="#e6007a",
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
    output=Output("aye_nay_chart_gov2", "figure"),
    inputs=[Input("specific-referenda-stats-gov2", "data")],
)
def aye_nay_chart_gov2(referendum_data):
    if referendum_data:
        df_referenda = pd.DataFrame(referendum_data)
        df_referenda["voted_amount_with_conviction_aye_perc"] = round(
            df_referenda["voted_amount_with_conviction_aye"]
            / df_referenda["voted_amount_with_conviction_total"]
            * 100,
            2,
        )
        df_referenda["voted_amount_with_conviction_nay_perc"] = round(
            df_referenda["voted_amount_with_conviction_nay"]
            / df_referenda["voted_amount_with_conviction_total"]
            * 100,
            2,
        )
        third_graph_data = [
            go.Bar(
                name="Aye Votes",
                x=df_referenda["voted_amount_with_conviction_aye_perc"],
                y=["referendum_index"],
                textposition="auto",
                orientation="h",
                marker_color="#ffffff",
                texttemplate="<b>%{x} %</b>",
            ),
            go.Bar(
                name="Aye Votes",
                x=df_referenda["voted_amount_with_conviction_nay_perc"],
                y=["referendum_index"],
                textposition="auto",
                orientation="h",
                marker_color="#e6007a",
                texttemplate="<b>%{x} %</b>",
                textangle=0,
                textfont_color="white",
            ),
        ]
        annotations = []
        space = 0
        for x, category in zip(
            [
                df_referenda["voted_amount_with_conviction_aye_perc"].values[0],
                df_referenda["voted_amount_with_conviction_nay_perc"].values[0],
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
    output=Output("delegation_chart_gov2", "figure"),
    inputs=[Input("specific-referenda-stats-gov2", "data")],
)
def aye_nay_chart_gov2(referendum_data):
    if referendum_data:
        df_referenda = pd.DataFrame(referendum_data)
        df_referenda["voted_amount_with_conviction_direct_perc"] = round(
            df_referenda["voted_amount_with_conviction_direct"]
            / (
                df_referenda["voted_amount_with_conviction_delegated"]
                + df_referenda["voted_amount_with_conviction_direct"]
            )
            * 100,
            2,
        )
        df_referenda["voted_amount_with_conviction_delegated_perc"] = round(
            df_referenda["voted_amount_with_conviction_delegated"]
            / (
                df_referenda["voted_amount_with_conviction_delegated"]
                + df_referenda["voted_amount_with_conviction_direct"]
            )
            * 100,
            2,
        )
        third_graph_data = [
            go.Bar(
                name="Direct Votes",
                x=df_referenda["voted_amount_with_conviction_direct_perc"],
                y=["referendum_index"],
                textposition="inside",
                orientation="h",
                marker_color="#ffffff",
                texttemplate="<b>%{x} %</b>",
            ),
            go.Bar(
                name="Delegated Votes",
                x=df_referenda["voted_amount_with_conviction_delegated_perc"],
                y=["referendum_index"],
                textposition="inside",
                orientation="h",
                marker_color="#e6007a",
                texttemplate="<b>%{x} %</b>",
                textangle=0,
            ),
        ]
        annotations = []
        space = 0
        for x, category in zip(
            [
                df_referenda["voted_amount_with_conviction_direct_perc"].values[0],
                df_referenda["voted_amount_with_conviction_delegated_perc"].values[0],
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
    output=Output("voter_type_chart_gov2", "figure"),
    inputs=[Input("specific-referenda-stats-gov2", "data")],
)
def aye_nay_chart_gov2(referendum_data):
    if referendum_data:
        df_referenda = pd.DataFrame(referendum_data)
        df_referenda["voted_amount_with_conviction_validator_perc"] = round(
            df_referenda["voted_amount_with_conviction_validator"]
            / (
                df_referenda["voted_amount_with_conviction_validator"]
                + df_referenda["voted_amount_with_conviction_normal"]
            )
            * 100,
            2,
        )
        df_referenda["voted_amount_with_conviction_normal_perc"] = round(
            df_referenda["voted_amount_with_conviction_normal"]
            / (
                df_referenda["voted_amount_with_conviction_validator"]
                + df_referenda["voted_amount_with_conviction_normal"]
            )
            * 100,
            2,
        )
        third_graph_data = [
            go.Bar(
                name="Validator Votes",
                x=df_referenda["voted_amount_with_conviction_validator_perc"],
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
                x=df_referenda["voted_amount_with_conviction_normal_perc"],
                y=["referendum_index"],
                textposition="inside",
                orientation="h",
                marker_color="#ffffff",
                texttemplate="<b>%{x} %</b>",
                textangle=0,
            ),
        ]
        annotations = []
        space = 0
        for x, category in zip(
            [
                df_referenda["voted_amount_with_conviction_validator_perc"].values[0],
                df_referenda["voted_amount_with_conviction_normal_perc"].values[0],
            ],
            ["Validator", "Normal"],
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
    Output("top-5-delegated-table-gov2", "children"),
    inputs=[Input("specific-referendum-data-gov2", "data")],
)
def create_top_5_delegtation_table(referendum_data_data):
    df = pd.DataFrame(referendum_data_data)
    df = (
        df.groupby(["delegated_to", "decision"])["voted_amount_with_conviction"]
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
    )
    return my_table


@app.callback(
    Output("top-5-direct-voter-table-gov2", "children"),
    inputs=[Input("specific-referendum-data-gov2", "data")],
)
def create_top_5_direct_voter_table(referendum_data_data):
    df = pd.DataFrame(referendum_data_data)
    df = (
        df[df["delegated_to"].isnull()]
        .sort_values(by="voted_amount_with_conviction", ascending=False)
        .head()
        .reset_index()[["voter", "decision", "voted_amount_with_conviction"]]
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
                        "column_id": "voter",
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
            "fontSize": 12,
            "fontFamily": "Unbounded Blond",
        },
        style_header={"backgroundColor": "#161a28", "color": "darkgray"},
        style_data={"backgroundColor": "#161a28", "color": "white"},
    )
    return my_table
