from dash import html
from dash import dcc
import dash_daq as daq
import pandas as pd
from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from utils.data_preparation import (
    preprocessing_referendum,
    preprocessing_votes,
    get_df_new_accounts,
    get_substrate_live_data,
)


def build_tab_1():
    return [
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(className="section-banner", children="Ongoing Referenda"),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            id="live-data-table",
            className="twelve columns",
            children=[],
        ),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(className="section-banner", children="Past Referenda"),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            children=[
                html.Div([], className="one column"),
                # rangebar
                html.Div(
                    id="id-rangebar",
                    className="ten columns",
                    children=[
                        "Loading",
                        dcc.RangeSlider(id="selected-ids", min=0, max=20, marks=None),
                    ],
                ),
                html.Div([], className="one column"),
            ]
        ),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            className="twelve columns",
            children=[
                html.Div(
                    className="six columns graph-block",
                    children=[
                        html.Div(
                            className="twelve columns",
                            children=[
                                daq.ToggleSwitch(
                                    id="votes_counts_chart_selection",
                                    label=["Votes Split", "Duration"],
                                    value=True,
                                )
                            ],
                        ),
                        html.Div(
                            id="first-chart",
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(dcc.Graph(id="votes_counts_barchart"))
                                    ],
                                    type="default",
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="six columns",
                    children=[
                        html.Div(
                            className="seven columns",
                            children=[
                                html.H4(
                                    "Turnout",
                                    className="graph__title",
                                )
                            ],
                        ),
                        html.Div(
                            className="four columns",
                            children=[
                                daq.ToggleSwitch(
                                    id="turn_out_chart_selection",
                                    label=["Absolute", "Percentage"],
                                    value=True,
                                )
                            ],
                        ),
                        html.Div(
                            id="second-chart",
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(dcc.Graph(id="turnout_scatterchart"))
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
            children=[
                html.Div(
                    id="third-chart",
                    className="six columns",
                    children=[
                        dcc.Loading(
                            id="loading-icon",
                            children=[html.Div(dcc.Graph(id="new_accounts_barchart"))],
                            type="default",
                        )
                    ],
                ),
                html.Div(
                    id="forth-chart",
                    className="six columns",
                    children=[
                        dcc.Loading(
                            id="loading-icon",
                            children=[html.Div(dcc.Graph(id="voted_ksm_scatterchart"))],
                            type="default",
                        )
                    ],
                ),
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    id="first-pie-chart",
                    className="six columns",
                    children=[
                        dcc.Loading(
                            id="loading-icon",
                            children=[html.Div(dcc.Graph(id="call_module_piechart"))],
                            type="default",
                        )
                    ],
                ),
                html.Div(
                    id="table-placeholder",
                    className="five columns",
                    children=[],
                ),
            ]
        ),
    ]


#
# def generate_votes_counts_chart():
#     return dcc.Graph(
#         id="votes_counts_barchart",
#         figure={
#             "data": [
#                 {
#                     "labels": [],
#                     "values": [],
#                     "marker": {"line": {"color": "white", "width": 1}},
#                     "hoverinfo": "label",
#                     "textinfo": "label",
#                 }
#             ],
#             "layout": {
#                 "title": "<b>Vote Count</b>",
#                 "barmode": "stack",
#                 "paper_bgcolor": "#161a28",
#                 "plot_bgcolor": "#161a28",
#                 "xaxis": dict(title="Referendum ID", linecolor="#BCCCDC"),
#                 "yaxis": dict(title="Vote counts", linecolor="#021C1E"),
#                 "yaxis2": dict(
#                     title="Duration of voting",
#                     linecolor="#021C1E",
#                     anchor="x",
#                     overlaying="y",
#                     side="right",
#                 ),
#                 "legend": dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
#                 "template": "plotly_dark",
#             },
#         },
#     )


def generate_turnout_chart():
    return dcc.Graph(
        id="turnout_scatterchart",
        figure={
            "data": [
                {
                    "x": [],
                    "y": [],
                    "mode": "lines+markers",
                    "line": {"color": "#f4d44d"},
                    # rgb(0, 0, 100)
                    "marker": dict(color="rgb(0, 0, 100)", size=8),
                    "hovertemplate": "Referendum id: %{x:.0f}<br>"
                    + "Turnout (%): %{y:.4f}<br>"
                    + "<extra></extra>",
                }
            ],
            "layout": {
                "title": "<b>Turnout for selected Referendum IDs</b>",
                "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                # rgb(248, 248, 255)
                "plot_bgcolor": "rgba(0,0,0,0)",
                # rgb(248, 248, 255)
                "font": {"color": "white"},
                "autosize": True,
                "barmode": "stack",
                "xaxis": dict(title="Referendum ID", linecolor="#BCCCDC"),
                "yaxis": dict(
                    title="Turnout (% of total issued Kusama)", linecolor="#021C1E"
                ),
                "legend": dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            },
        },
    )


def generate_new_accouts_chart():
    return dcc.Graph(
        id="new_accounts_barchart",
        figure={
            "data": [],
            "layout": {
                "title": "<b>New accounts counts for selected Referendum IDs</b>",
                "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
                "barmode": "stack",
                "xaxis": dict(title="Referendum ID", linecolor="#BCCCDC"),
                "yaxis": dict(title="New accounts counts", linecolor="#021C1E"),
                "yaxis2": dict(
                    title="New accounts counts (% of total votes counts)",
                    linecolor="#021C1E",
                    anchor="x",
                    overlaying="y",
                    side="right",
                ),
                "legend": dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            },
        },
    )


def generate_voted_ksm_graph():
    return dcc.Graph(
        id="voted_ksm_scatterchart",
        figure={
            "data": [],
            "layout": {
                "title": "<b>Voted KSM with conviction Mean and Median for selected Referendum IDs</b>",
                "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                # rgb(248, 248, 255)
                "plot_bgcolor": "rgba(0,0,0,0)",
                # rgb(248, 248, 255)
                "font": {"color": "white"},
                "autosize": True,
                "barmode": "stack",
                "xaxis": dict(title="Referendum ID", linecolor="#BCCCDC"),
                "yaxis": dict(title="Locked KSM - Mean", linecolor="#021C1E"),
                "yaxis2": dict(
                    title="Locked KSM - Median & Quantile",
                    linecolor="#021C1E",
                    anchor="x",
                    overlaying="y",
                    side="right",
                ),
                "legend": dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            },
        },
    )


def generate_piechart():
    return dcc.Graph(
        id="call_module_piechart",
        figure={
            "data": [
                {
                    "labels": [],
                    "values": [],
                    "type": "pie",
                    "marker": {"line": {"color": "white", "width": 1}},
                    "hoverinfo": "label",
                    "textinfo": "label",
                }
            ],
            "layout": {
                "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
            },
        },
    )
