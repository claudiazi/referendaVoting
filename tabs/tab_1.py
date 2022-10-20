import time

import dash_daq as daq
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from config import (
    voting_group_dict,
    voting_group_perc_dict,
    voting_group_colors,
    color_scale,
)
from utils.plotting import data_perc_bars, blank_figure


def build_tab_1():
    return [
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(className="section-banner", children="Ongoing Referenda"),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            className="twelve columns",
            children=[
                dcc.Loading(
                    html.Div(
                        id="live-data-table",
                        children=[],
                    )
                )
            ],
        ),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(className="section-banner", children="All Referenda"),
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
                                    className="toggle_switch",
                                    label=["Votes Split", "Duration"],
                                    value=False,
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
                                        html.Div(
                                            dcc.Graph(
                                                id="votes_counts_barchart",
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
                                daq.ToggleSwitch(
                                    id="turn_out_chart_selection",
                                    className="toggle_switch",
                                    label=["Absolute", "Percentage"],
                                    value=False,
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
                                        html.Div(
                                            dcc.Graph(
                                                id="turnout_scatterchart",
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
                            className="twelve columns",
                            children=[
                                daq.ToggleSwitch(
                                    id="new_accounts_selection",
                                    className="toggle_switch",
                                    label=["Absolute", "Percentage"],
                                    value=False,
                                )
                            ],
                        ),
                        html.Div(
                            id="third-chart",
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(
                                            dcc.Graph(
                                                id="new_accounts_barchart",
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
                    className="six columns graph-block",
                    children=[
                        html.Div(
                            className="twelve columns",
                            children=[
                                daq.ToggleSwitch(
                                    id="conviction_selection",
                                    label=["Mean", "Median"],
                                    value=False,
                                )
                            ],
                        ),
                        html.Div(
                            id="forth-chart",
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(
                                            dcc.Graph(
                                                id="voted_ksm_scatterchart",
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
                            className="twelve columns",
                            children=[
                                daq.ToggleSwitch(
                                    id="delegated_chart_selection",
                                    className="toggle_switch",
                                    label=["Votes Split", "Voted Amount Split"],
                                    value=False,
                                )
                            ],
                        ),
                        html.Div(
                            id="v-chart",
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(
                                            dcc.Graph(
                                                id="delegation_barchart",
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
                            id="vi-chart",
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(
                                            dcc.Graph(
                                                id="threshold_piechart",
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
                            className="twelve columns",
                            children=[
                                daq.ToggleSwitch(
                                    id="voting_time_selection",
                                    label=["Absolute", "Percentage"],
                                    value=False,
                                )
                            ],
                        ),
                        html.Div(
                            id="fifth-chart",
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(
                                            dcc.Graph(
                                                id="voting_time_barchart",
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
                    className="six columns graph-block",
                    children=[
                        html.Div(
                            id="sixth-chart",
                            className="twelve columns",
                            children=[
                                html.Div(
                                    className="twelve columns", children=[html.Br()]
                                ),
                                html.Div(
                                    id="fifth-chart",
                                    className="twelve columns",
                                    children=[
                                        dcc.Loading(
                                            id="loading-icon",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="vote_timing_distribution",
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
            ],
        ),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            children=[
                html.Div(
                    id="section-piechart",
                    className="six columns graph-block",
                    children=[
                        dcc.Loading(
                            id="loading-icon",
                            children=[
                                html.Div(
                                    dcc.Graph(
                                        id="section_piechart",
                                        figure=blank_figure(),
                                    )
                                ),
                                html.Button(
                                    "Clear Selection",
                                    id="clear-radio",
                                    className="click-button",
                                ),
                            ],
                            type="default",
                        )
                    ],
                ),
                html.Div(
                    id="section-piechart",
                    className="six columns graph-block",
                    children=[
                        dcc.Loading(
                            id="loading-icon",
                            children=[
                                html.Div(
                                    dcc.Graph(
                                        id="method_piechart",
                                        figure=blank_figure(),
                                    )
                                )
                            ],
                            type="default",
                        )
                    ],
                ),
            ]
        ),
        html.Div(
            className="twelve columns",
            children=[
                html.Div(
                    className="six columns graph-block",
                    children=[
                        html.Div(className="twelve columns", children=[html.Br()]),
                        html.Div(
                            id="fifth-chart",
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(
                                            dcc.Graph(
                                                id="proposer_piechart",
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
                    className="six columns graph-block",
                    children=[
                        html.Div(
                            className="twelve columns",
                            children=[
                                daq.ToggleSwitch(
                                    id="quiz_selection",
                                    className="toggle_switch",
                                    label=["Absolute", "Percentage"],
                                    value=False,
                                )
                            ],
                        ),
                        html.Div(
                            id="xii-chart",
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(
                                            dcc.Graph(
                                                id="quiz_answers_barchart",
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


layout = build_tab_1()


@app.callback(
    Output("id-rangebar", "children"),
    [Input("full-referenda-data", "data")],
)
def create_rangeslider(closed_referenda_data):
    df = pd.DataFrame(closed_referenda_data)
    range_min = df["referendum_index"].min()
    range_max = df["referendum_index"].max()
    return dcc.RangeSlider(
        id="selected-ids",
        min=range_min,
        max=range_max,
        value=[160, range_max],
        tooltip={"placement": "top", "always_visible": True},
    )


@app.callback(
    Output("live-data-table", "children"), [Input("ongoing-referenda-data", "data")]
)
def create_live_data_table(ongoing_referenda_data):
    df = pd.DataFrame(ongoing_referenda_data)
    print(f"live data updated {time.time()}")
    df["voted_amount_aye_perc"] = (
        df["voted_amount_aye"] / df["voted_amount_total"] * 100
    )
    df["voted_amount_nay_perc"] = (
        df["voted_amount_nay"] / df["voted_amount_total"] * 100
    )
    df["turnout_total_perc"] = df["turnout_total_perc"].apply(lambda x: f"{x:.2f} %")
    df["voted_amount_aye"] = df.apply(
        lambda x: f"{x['voted_amount_aye']} ({x['voted_amount_aye_perc']:.2f} %)",
        axis=1,
    )
    df["voted_amount_nay"] = df.apply(
        lambda x: f"{x['voted_amount_nay']} ({x['voted_amount_nay_perc']:.2f} %)",
        axis=1,
    )
    df = df[
        [
            "referendum_index",
            "section",
            "turnout_total_perc",
            "voted_amount_aye",
            "voted_amount_nay",
        ]
    ]
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


# Update first chart
@app.callback(
    output=Output("votes_counts_barchart", "figure"),
    inputs=[
        Input("interval-component", "n_intervals"),
        Input("selected-ids", "value"),
        Input("votes_counts_chart_selection", "value"),
        Input("section_piechart", "clickData"),
    ],
    state=Input("full-referenda-data", "data"),
)
def update_votes_counts_chart(
    n_intervals,
    selected_ids,
    selected_toggle_value,
    click_selected_section,
    referenda_data,
):
    df_referenda = pd.DataFrame(referenda_data).sort_values(by="referendum_index")
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    if click_selected_section:
        click_selected_section = click_selected_section["points"][0]["label"]
        df_referenda = df_referenda[df_referenda["section"] == click_selected_section]
    first_graph_layout = go.Layout(
        title="<b>Vote Count</b>",
        barmode="stack",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Vote counts", linecolor="#021C1E"),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        template="plotly_dark",
        hovermode="x",
    )
    if selected_toggle_value == False:
        first_graph_data = [
            go.Bar(
                name="Aye Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_aye"],
                marker_color="#ffffff",
                customdata=df_referenda["count_total"],
                opacity=0.8,
                # hovertemplate="<b>Aye Votes</b><br><br>"
                # + "Vote count: %{y:.0f}<br>"
                # + "Total counts: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
            go.Bar(
                name="Nay Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_nay"],
                customdata=df_referenda["count_total"],
                marker_color="#e6007a",
                opacity=0.8,
                # hovertemplate="<b>Nay Votes</b><br><br>"
                # + "Vote count: %{y:.0f}<br>"
                # + "Total counts: %{customdata:.0f}<br>"
                # + "<extra></extra>",
            ),
        ]
    if selected_toggle_value == True:
        first_graph_data = [
            go.Bar(
                name="Total Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_total"],
                customdata=[
                    f"{x * 24:.2f} hours" if x < 1 else f"{x:.2f} days"
                    for x in df_referenda["vote_duration"]
                ],
                marker=dict(
                    color=df_referenda[
                        "vote_duration"
                    ],  # set color equal to a variable # one of plotly colorscales
                    colorscale=[
                        [0, "#ffe6f5"],
                        [0.1, "#ffb3e0"],
                        [0.2, "#ff99d6"],
                        [0.3, "#ff80cc"],
                        [0.4, "#ff66c2"],
                        [0.5, "#ff4db8"],
                        [0.6, "#ff33ad"],
                        [0.7, "#ff1aa3"],
                        [0.8, "#e6007a"],
                        [0.9, "#cc007a"],
                        [1, "#b3006b"],
                    ],
                    showscale=True,
                ),
                opacity=0.8,
                hovertemplate="<b>Referendum %{x}</b><br><br>"
                + "Duration: %{customdata} <br>"
                + "Total counts: %{y:.0f}<br>"
                + "<extra></extra>",
            ),
        ]
    fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
    return fig_first_graph


# Update second chart
@app.callback(
    output=Output("turnout_scatterchart", "figure"),
    inputs=[Input("turn_out_chart_selection", "value")],
    state=[Input("full-referenda-data", "data"), Input("selected-ids", "value")],
)
def update_bar_chart(selected_toggle_value, referenda_data, selected_ids):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    if selected_toggle_value == False:
        second_graph_data = [
            go.Scatter(
                name="Aye Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["voted_amount_aye"],
                marker_color="#ffffff",
                fill="tozeroy",
                customdata=df_referenda["voted_amount_total"],
                stackgroup="one",  # define stack group
                hovertemplate="<b>Aye Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Aye amount: %{y:.1f}<br>"
                + "Turnout: %{customdata:.2f}<br>"
                + "<extra></extra>",
            ),
            go.Scatter(
                name="Nay Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["voted_amount_nay"],
                customdata=df_referenda["voted_amount_total"],
                marker_color="#e6007a",
                fill="tonexty",
                stackgroup="one",  # define stack group
                hovertemplate="<b>Nay Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Nay Amount: %{y:.1f}<br>"
                + "Turnout: %{customdata:.2f}<br>"
                + "<extra></extra>",
            ),
        ]
    else:
        second_graph_data = [
            go.Bar(
                name="Aye Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["turnout_aye_perc"],
                marker_color="#ffffff",
                opacity=0.8,
                customdata=df_referenda["turnout_total_perc"],
                hovertemplate="<b>Aye Votes</b><br><br>"
                + "Referendum id: %{x:.0f}<br>"
                + "Turnout perc - aye: %{y:.2f}<br>"
                + "Turnout perc: %{customdata:.2f}<br>"
                + "<extra></extra>",
            ),
            go.Bar(
                name="Nay Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["turnout_nay_perc"],
                opacity=0.8,
                customdata=df_referenda["turnout_total_perc"],
                marker_color="#e6007a",
                hovertemplate="<b>Nay Votes</b><br><br>"
                + "Referendum id: %{x:.0f}<br>"
                + "Turnout perc - nay: %{y:.2f}<br>"
                + "Turnout perc: %{customdata:.2f}<br>"
                + "<extra></extra>",
            ),
        ]

    second_graph_layout = go.Layout(
        title="<b>Turnout</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Turnout (% of total issued Kusama)", linecolor="#021C1E"),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
        template="plotly_dark",
        hovermode="x",
    )
    fig_second_graph = go.Figure(data=second_graph_data, layout=second_graph_layout)
    return fig_second_graph


# Update third chart
@app.callback(
    output=Output("new_accounts_barchart", "figure"),
    inputs=[Input("new_accounts_selection", "value")],
    state=[
        Input("full-referenda-data", "data"),
        Input("selected-ids", "value"),
    ],
)
def update_new_accounts_chart(selected_toggle_value, referenda_data, selected_ids):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    if selected_toggle_value == False:
        third_graph_data = [
            go.Bar(
                name="New accounts counts",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_new"],
                marker_color="#e6007a",
                opacity=0.8,
                hovertemplate="Referendum id: %{x:.0f}<br>"
                + "New accounts counts: %{y:.0f}<br>"
                + "<extra></extra>",
            ),
        ]
    else:
        third_graph_data = [
            go.Scatter(
                name="% of total votes counts",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_new_perc"],
                # mode="lines+markers",
                line=dict(color="#e6007a"),
                opacity=0.8,
                # marker=dict(color="rgb(0, 0, 100)", size=4),
                hovertemplate="Referendum id: %{x:.0f}<br>"
                + "% of total votes counts: %{y:.4f}<br>"
                + "<extra></extra>",
            ),
        ]
    third_graph_layout = go.Layout(
        title="<b>New Accounts</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="New accounts counts", linecolor="#021C1E"),
        # yaxis2=dict(
        #     title="New accounts counts (% of total votes counts)",
        #     linecolor="#021C1E",
        #     anchor="x",
        #     overlaying="y",
        #     side="right",
        # ),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        template="plotly_dark",
    )

    fig_third_graph = go.Figure(data=third_graph_data, layout=third_graph_layout)
    return fig_third_graph


# Update forth chart
@app.callback(
    output=Output("voted_ksm_scatterchart", "figure"),
    inputs=[Input("conviction_selection", "value")],
    state=[Input("full-referenda-data", "data"), Input("selected-ids", "value")],
)
def update_vote_amount_with_conviction_chart(
    selected_toggle_value, referenda_data, selected_ids
):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    if selected_toggle_value == False:
        forth_graph_data = [
            go.Scatter(
                name="mean",
                x=df_referenda["referendum_index"],
                y=df_referenda["conviction_mean"],
                mode="lines+markers",
                line=dict(color="#e6007a"),
                marker=dict(color="#e6007a", size=4),
                opacity=0.8,
                hovertemplate="Referendum %{x:.0f}<br>"
                + "conviction mean: %{y:.3f}<br>"
                + "<extra></extra>",
            ),
        ]
        yaxis_name = "Conviction - Mean"
    else:
        forth_graph_data = [
            go.Scatter(
                name="median",
                x=df_referenda["referendum_index"],
                y=df_referenda["conviction_median"],
                mode="lines+markers",
                line=dict(color="#e6007a"),
                marker=dict(color="#e6007a", size=4),
                opacity=0.8,
                hovertemplate="Referendum %{x:.0f}<br>"
                + "Conviction median: %{y:.3f}<br>"
                + "<extra></extra>",
            ),
        ]
        yaxis_name = "Conviction - Median"

    forth_graph_layout = go.Layout(
        title="<b>Conviction Median</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        template="plotly_dark",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title=yaxis_name, linecolor="#021C1E"),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )
    fig_forth_graph = go.Figure(data=forth_graph_data, layout=forth_graph_layout)
    return fig_forth_graph


# Update v chart
@app.callback(
    output=Output("delegation_barchart", "figure"),
    inputs=[Input("delegated_chart_selection", "value")],
    state=[Input("full-referenda-data", "data"), Input("selected-ids", "value")],
)
def update_delegation_chart(selected_toggle_value, referenda_data, selected_ids):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    if selected_toggle_value == False:
        v_graph_data = [
            go.Scatter(
                name="Direct Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_direct"],
                marker_color="#ffffff",
                fill="tozeroy",
                customdata=df_referenda["count_total"],
                stackgroup="one",  # define stack group
                hovertemplate="<b>Direct Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Count direct votes: %{y:.0f}<br>"
                + "Count total: %{customdata:.0f}<br>"
                + "<extra></extra>",
            ),
            go.Scatter(
                name="Delegated Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_delegated"],
                customdata=df_referenda["count_total"],
                marker_color="#e6007a",
                fill="tonexty",
                stackgroup="one",  # define stack group
                hovertemplate="<b>Delegated Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Count delegated votes: %{y:.0f}<br>"
                + "Count total: %{customdata:.0f}<br>"
                + "<extra></extra>",
            ),
        ]
        yaxis_name = "Vote Count"
    else:
        v_graph_data = [
            go.Scatter(
                name="Direct Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["voted_amount_direct"],
                marker_color="#ffffff",
                fill="tozeroy",
                stackgroup="one",  # define stack group
                customdata=df_referenda["voted_amount_total"],
                hovertemplate="<b>Direct Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Voted amount - Direct: %{y:.0f}<br>"
                + "Voted amount - Total: %{customdata:.0f}<br>"
                + "<extra></extra>",
            ),
            go.Scatter(
                name="Delegated Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["voted_amount_delegated"],
                customdata=df_referenda["voted_amount_total"],
                marker_color="#e6007a",
                fill="tozeroy",
                stackgroup="one",  # define stack group
                hovertemplate="<b>Delegated Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Voted amount - Delegated: %{y:.0f}<br>"
                + "Voted amount - Total: %{customdata:.0f}<br>"
                + "<extra></extra>",
            ),
        ]
        yaxis_name = "Voted Amount"

    v_graph_layout = go.Layout(
        title="<b>Turnout</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title=yaxis_name, linecolor="#021C1E"),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
        template="plotly_dark",
        hovermode="x",
    )
    fig_v_graph = go.Figure(data=v_graph_data, layout=v_graph_layout)
    return fig_v_graph


# Update fifth chart
@app.callback(
    output=Output("voting_time_barchart", "figure"),
    inputs=[Input("voting_time_selection", "value")],
    state=[Input("full-referenda-data", "data"), Input("selected-ids", "value")],
)
def update_voting_time_barchart(selected_toggle_value, referenda_data, selected_ids):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]

    if selected_toggle_value == False:
        fifth_graph_data = []
        for count, voting_time_group in enumerate(
            [
                "count_0_4_1_4_vote_duration",
                "count_1_4_2_4_vote_duration",
                "count_2_4_3_4_vote_duration",
                "count_3_4_4_4_vote_duration",
            ]
        ):
            fifth_graph_data.append(
                go.Bar(
                    x=df_referenda["referendum_index"],
                    y=df_referenda[voting_time_group],
                    name=f"{voting_group_dict[voting_time_group]}",
                    customdata=df_referenda["count_total"],
                    marker=dict(color=voting_group_colors[count]),
                    opacity=0.8,
                    # hovertemplate="Referendum id: %{x:.0f}<br>"
                    # + "Group count: %{y:.0f}<br>"
                    # + "Total: %{customdata:.0f}<br>"
                    # + "<extra></extra>",
                )
            )
        fifth_graph_layout = go.Layout(
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
    else:
        fifth_graph_data = []
        for count, voting_time_group in enumerate(
            [
                "count_0_4_1_4_vote_duration_perc",
                "count_1_4_2_4_vote_duration_perc",
                "count_2_4_3_4_vote_duration_perc",
                "count_3_4_4_4_vote_duration_perc",
            ]
        ):
            fifth_graph_data.append(
                go.Bar(
                    x=df_referenda["referendum_index"],
                    y=df_referenda[voting_time_group],
                    marker=dict(color=voting_group_colors[count]),
                    name=f"{voting_group_perc_dict[voting_time_group]}",
                    customdata=df_referenda["count_total"],
                    hovertemplate="%{y:.2f}",
                    opacity=0.8,
                )
            )
        fifth_graph_layout = go.Layout(
            title="<b>When Wallets Voted</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Count of voting time groups (%)", linecolor="#021C1E"),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
            template="plotly_dark",
            hovermode="x",
        )
    fig_fifth_graph = go.Figure(data=fifth_graph_data, layout=fifth_graph_layout)
    return fig_fifth_graph


# Update sixth chart
@app.callback(
    output=Output("vote_timing_distribution", "figure"),
    inputs=[
        Input("voting_time_selection", "value"),
        Input("section_piechart", "clickData"),
    ],
    state=[Input("full-referenda-data", "data"), Input("selected-ids", "value")],
)
def update_vote_timing_distribution(
    selected_toggle_value, click_selected_section, referenda_data, selected_ids
):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    df_voting_group_sum = df_referenda[
        [
            "count_0_4_1_4_vote_duration",
            "count_1_4_2_4_vote_duration",
            "count_2_4_3_4_vote_duration",
            "count_3_4_4_4_vote_duration",
        ]
    ].sum()
    sixth_graph_data = [
        go.Pie(
            labels=[voting_group_dict[key] for key in df_voting_group_sum.index],
            values=df_voting_group_sum.values,
            customdata=df_referenda["count_total"],
            marker=dict(colors=voting_group_colors),
            # hovertemplate="Referendum id: %{x:.0f}<br>"
            # + "Group count: %{y:.0f}<br>"
            # + "Total: %{customdata:.0f}<br>"
            # + "<extra></extra>",
        )
    ]
    sixth_graph_layout = go.Layout(
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

    fig_sixth_graph = go.Figure(data=sixth_graph_data, layout=sixth_graph_layout)
    return fig_sixth_graph


#
# Update ix chart
@app.callback(
    Output("section_piechart", "figure"),
    [Input("full-referenda-data", "data"), Input("selected-ids", "value")],
)
def update_pie_chart(referenda_data, selected_ids):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    df_section_group_count = df_referenda["section"].value_counts()
    ix_graph_data = [
        go.Pie(
            labels=df_section_group_count.index,
            values=df_section_group_count.values,
            marker=dict(colors=color_scale),
            textposition="inside",
            opacity=0.8,
            # hovertemplate="Referendum id: %{x:.0f}<br>"
            # + "Group count: %{y:.0f}<br>"
            # + "Total: %{customdata:.0f}<br>"
            # + "<extra></extra>",
        )
    ]
    ix_graph_layout = go.Layout(
        title="<b>Section</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
        template="plotly_dark",
        hovermode="x",
        autosize=True,
        clickmode="event+select",
    )
    fig_ix_graph = go.Figure(data=ix_graph_data, layout=ix_graph_layout)
    return fig_ix_graph


# Update x chart
@app.callback(
    Output("method_piechart", "figure"),
    [
        Input("full-referenda-data", "data"),
        Input("selected-ids", "value"),
        Input("section_piechart", "clickData"),
    ],
)
def update_pie_chart(referenda_data, selected_ids, click_selected_section):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    if click_selected_section:
        click_selected_section = click_selected_section["points"][0]["label"]
        df_referenda = df_referenda[df_referenda["section"] == click_selected_section]
    df_method_group_count = df_referenda["method"].value_counts()
    x_graph_data = [
        go.Pie(
            labels=df_method_group_count.index,
            values=df_method_group_count.values,
            marker=dict(colors=color_scale),
            textposition="inside",
            opacity=0.8,
            # hovertemplate="Referendum id: %{x:.0f}<br>"
            # + "Group count: %{y:.0f}<br>"
            # + "Total: %{customdata:.0f}<br>"
            # + "<extra></extra>",
        )
    ]
    x_graph_layout = go.Layout(
        title="<b>Method</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
        template="plotly_dark",
        hovermode="x",
        autosize=True,
        clickmode="event+select",
    )
    fig_x_graph = go.Figure(data=x_graph_data, layout=x_graph_layout)
    return fig_x_graph


# Update xi chart
@app.callback(
    Output("proposer_piechart", "figure"),
    [
        Input("full-referenda-data", "data"),
        Input("selected-ids", "value"),
        Input("section_piechart", "clickData"),
    ],
)
def update_pie_chart(referenda_data, selected_ids, click_selected_section):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    if click_selected_section:
        click_selected_section = click_selected_section["points"][0]["label"]
        df_referenda = df_referenda[df_referenda["section"] == click_selected_section]
    df_proposer_count = df_referenda["proposer"].value_counts()
    xi_graph_data = [
        go.Pie(
            labels=df_proposer_count.index,
            values=df_proposer_count.values,
            marker=dict(colors=color_scale),
            textposition="inside",
            # hovertemplate="Referendum id: %{x:.0f}<br>"
            # + "Group count: %{y:.0f}<br>"
            # + "Total: %{customdata:.0f}<br>"
            # + "<extra></extra>",
        )
    ]
    xi_graph_layout = go.Layout(
        title="<b>Proposer</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
        template="plotly_dark",
        hovermode="x",
        autosize=True,
        clickmode="event+select",
    )
    fig_xi_graph = go.Figure(data=xi_graph_data, layout=xi_graph_layout)
    return fig_xi_graph


# Update vi chart
@app.callback(
    Output("threshold_piechart", "figure"),
    [
        Input("full-referenda-data", "data"),
        Input("selected-ids", "value"),
    ],
)
def update_threshold_piechart(referenda_data, selected_ids):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    df_threshold_count = df_referenda["threshold_type"].value_counts()
    vi_graph_data = [
        go.Pie(
            labels=df_threshold_count.index,
            values=df_threshold_count.values,
            marker=dict(colors=["#e6007a", "#ffffff"]),
            textposition="inside",
            opacity=0.8,
            # hovertemplate="Referendum id: %{x:.0f}<br>"
            # + "Group count: %{y:.0f}<br>"
            # + "Total: %{customdata:.0f}<br>"
            # + "<extra></extra>",
        )
    ]
    vi_graph_layout = go.Layout(
        title="<b>Threshold Type</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
        template="plotly_dark",
        hovermode="x",
        autosize=True,
        clickmode="event+select",
    )
    fig_vi_graph = go.Figure(data=vi_graph_data, layout=vi_graph_layout)
    return fig_vi_graph


# Update xii chart
@app.callback(
    output=Output("quiz_answers_barchart", "figure"),
    inputs=[Input("quiz_selection", "value")],
    state=[
        Input("full-referenda-data", "data"),
        Input("selected-ids", "value"),
    ],
)
def update_quiz_answer_chart(selected_toggle_value, referenda_data, selected_ids):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    if selected_toggle_value == False:
        xii_graph_data = [
            go.Bar(
                name="Fully Correct Answers",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_fully_correct"],
                marker_color="#e6007a",
                hovertemplate="Referendum: %{x:.0f}<br>"
                + "Fully correct wallets: %{y:.0f}<br>"
                + "<extra></extra>",
            ),
        ]
        yaxis_name = "Count"
    else:
        xii_graph_data = [
            go.Scatter(
                name="% of Total Answers",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_fully_correct"]
                / df_referenda["count_quiz_attended_wallets"]
                * 100,
                # mode="lines+markers",
                line=dict(color="#e6007a"),
                # marker=dict(color="rgb(0, 0, 100)", size=4),
                hovertemplate="Referendum: %{x:.0f}<br>"
                + "% of total answers: %{y:.4f}<br>"
                + "<extra></extra>",
            ),
        ]
        yaxis_name = "% of Total Answers"
    xii_graph_layout = go.Layout(
        title="<b>Fully Correct Answers</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title=yaxis_name, linecolor="#021C1E"),
        # yaxis2=dict(
        #     title="New accounts counts (% of total votes counts)",
        #     linecolor="#021C1E",
        #     anchor="x",
        #     overlaying="y",
        #     side="right",
        # ),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        template="plotly_dark",
    )

    fig_xii_graph = go.Figure(data=xii_graph_data, layout=xii_graph_layout)
    return fig_xii_graph


@app.callback(
    Output("section_piechart", "clickData"),
    [Input("clear-radio", "n_clicks")],
)
def clear_section_selections(*args):
    return None


# # callback function for on_hover
# def hide_traces_on_hover(trace, points, selector):
#     if len(points.point_inds)==1: # identify hover
#         i = points.trace_index # get the index of the hovered trace
#         f.data[i].visible = True # keep the hovered trace visible
#         # create a list of traces you want to hide
#         hide_traces = [l_trace for idx, l_trace in enumerate(f.data) if idx != i]
#         for l_trace in hide_traces: # iterate over hide_traces
#             l_trace.visible = 'legendonly' # hide all remaining traces

# fig = go.FigureWidget() # create figure widget
# def hide_traces_on_click(fig, trace, points, selector):
#     if len(points.point_inds)==1: # identify hover
#         i = points.trace_index # get the index of the hovered trace
#         fig.data[i].visible = True # keep the hovered trace visible
#         # create a list of traces you want to hide
#         hide_traces = [l_trace for idx, l_trace in enumerate(f.data) if idx != i]
#         for l_trace in hide_traces: # iterate over hide_traces
#             l_trace.visible = 'legendonly' # hide all remaining traces
# import plotly.express as px
#
# def get_figure(x, y, selectedpoints, selectedpoints_local):
#
#     fig = px.pie(labels=x,values=y)
#     fig.update_traces(selectedpoints=selectedpoints, unselected={'marker': { 'opacity': 0.3 }, 'textfont': { 'color': 'rgba(0, 0, 0, 0)' } })
#
#     fig.update_layout(title="<b>Section</b>",
#         paper_bgcolor="#161a28",
#         plot_bgcolor="#161a28",
#         legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
#         template="plotly_dark",
#         hovermode="x",
#         autosize=True,
#         clickmode="event+select")
#
#     return fig
#
#
# @app.callback(
#     Output("section_piechart", "figure"),
#     [Input("full-referenda-data", "data"), Input("selected-ids", "value"), Input("section_piechart", "clickData")],
# )
# def update_pie_chart(referenda_data, selected_ids, selected_section):
#     df_referenda = pd.DataFrame(referenda_data)
#     if selected_ids:
#         df_referenda = df_referenda[
#             (df_referenda["referendum_index"] >= selected_ids[0])
#             & (df_referenda["referendum_index"] <= selected_ids[1])
#         ]
#     df_section_group_count = df_referenda["section"].value_counts()
#     all_secions = df_referenda["section"].unique()
#     return get_figure(df_section_group_count, df_section_group_count.index, df_section_group_count.values, all_secions, selected_section)
