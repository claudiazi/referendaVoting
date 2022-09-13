import time

import dash_daq as daq
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from utils.data_preparation import (
    get_df_new_accounts,
    get_substrate_live_data,
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
                                    className="toggle_switch",
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
                    className="six columns",
                    children=[
                        html.Div(
                            className="twelve columns",
                            children=[
                                daq.ToggleSwitch(
                                    id="turn_out_chart_selection",
                                    className="toggle_switch",
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
                    className="six columns",
                    children=[
                        html.Div(
                            className="twelve columns",
                            children=[
                                daq.ToggleSwitch(
                                    id="new_accounts_selection",
                                    className="toggle_switch",
                                    label=["Absolute", "Percentage"],
                                    value=True,
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
                    className="six columns",
                    children=[
                        html.Div(
                            className="twelve columns",
                            children=[
                                daq.ToggleSwitch(
                                    id="conviction_selection",
                                    label=["Mean", "Median"],
                                    value=True,
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
                                        html.Div(dcc.Graph(id="voted_ksm_scatterchart"))
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


layout = build_tab_1()


@app.callback(
    Output("id-rangebar", "children"),
    [Input("referenda-data", "data")],
)
def create_rangeslider(refined_referenda_data):
    df = pd.DataFrame(refined_referenda_data)
    range_min = df["referendum_index"].min()
    range_max = df["referendum_index"].max()
    return dcc.RangeSlider(id="selected-ids", min=range_min, max=range_max)


# Callback to update the live data
@app.callback(
    Output("ongoing-referenda-data", "data"),
    Input("interval-component-live", "n_intervals"),
)
def update_live_data(n_intervals):
    if n_intervals >= 0:
        df_ongoing_referenda = get_substrate_live_data()
        return df_ongoing_referenda.to_dict("record")


@app.callback(
    Output("live-data-table", "children"), Input("ongoing-referenda-data", "data")
)
def create_live_data_table(data):
    dff = pd.DataFrame(data[:])
    print(f"live data updated {time.time()}")
    dff = dff[["referendum_index", "threshold", "ayes_perc", "turnout"]]

    my_table = dash_table.DataTable(
        data=dff.to_dict("records"),
        columns=[{"name": i, "id": i} for i in dff.columns],
        sort_action="native",
        style_data_conditional=(
            [
                {
                    "if": {
                        "column_id": "referendum_index",
                    },
                    "fontWeight": "bold",
                    "color": "black",
                }
            ]
            + data_perc_bars(dff, "ayes_perc")
        ),
        style_cell={
            "width": "100px",
            "minWidth": "100px",
            "maxWidth": "100px",
            "overflow": "hidden",
            "textOverflow": "ellipsis",
        },
    )
    return my_table


@app.callback(
    Output("table-placeholder", "children"),
    [Input("referenda-data", "data"), Input("selected-ids", "value")],
)
def create_graph1(data, selected_ids):
    dff = pd.DataFrame(data[:])
    if selected_ids:
        dff = dff[
            (dff["referendum_index"] >= selected_ids[0])
            & (dff["referendum_index"] <= selected_ids[1])
        ]
    dff = dff[["referendum_index", "turnout_perc"]]
    # 2. convert string like JSON to pandas dataframe
    # dff = pd.read_json(data, orient='split')
    my_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in dff.columns], data=dff.to_dict("records")
    )
    return my_table


# Update first chart
@app.callback(
    output=Output("votes_counts_barchart", "figure"),
    inputs=[
        Input("interval-component", "n_intervals"),
        Input("selected-ids", "value"),
        Input("votes_counts_chart_selection", "value"),
    ],
    state=[Input("votes-data", "data"), Input("referenda-data", "data")],
)
def update_votes_counts_chart(
    n_intervals, selected_ids, selected_toggle_value, votes_data, referenda_data
):
    df_votes = pd.DataFrame(votes_data)
    df_referenda = pd.DataFrame(referenda_data).sort_values(by="referendum_index")
    if selected_ids:
        df_votes = df_votes[
            (df_votes["referendum_index"] >= selected_ids[0])
            & (df_votes["referendum_index"] <= selected_ids[1])
        ]

    df_counts_sum = (
        df_votes.groupby("referendum_index")["account_address"]
        .count()
        .reset_index(name="vote_counts")
        .sort_values(by="referendum_index")
    )
    df_counts_sum = df_counts_sum.merge(
        df_referenda, how="inner", on="referendum_index"
    ).sort_values(by="referendum_index")
    first_graph_layout = go.Layout(
        title="<b>Vote Count</b>",
        barmode="stack",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Vote counts", linecolor="#021C1E"),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        template="plotly_dark",
    )
    if selected_toggle_value == False:
        df_aye = df_votes[df_votes["passed"] == True]
        df_aye_count_sum = (
            df_aye.groupby("referendum_index")["account_address"]
            .count()
            .reset_index(name="vote_counts")
            .sort_values(by="referendum_index")
        )
        df_nay = df_votes[df_votes["passed"] == False]
        df_nay_count_sum = (
            df_nay.groupby("referendum_index")["account_address"]
            .count()
            .reset_index(name="vote_counts")
            .sort_values(by="referendum_index")
        )
        first_graph_data = [
            go.Bar(
                name="Aye Votes",
                x=df_aye_count_sum["referendum_index"],
                y=df_aye_count_sum["vote_counts"],
                marker_color="rgb(0, 0, 100)",
                customdata=df_counts_sum["vote_counts"],
                hovertemplate="<b>Aye Votes</b><br><br>"
                + "Referendum id: %{x:.0f}<br>"
                + "Aye vote counts: %{y:.0f}<br>"
                + "Total counts: %{customdata:.0f}<br>"
                + "<extra></extra>",
            ),
            go.Bar(
                name="Nay Votes",
                x=df_nay_count_sum["referendum_index"],
                y=df_nay_count_sum["vote_counts"],
                customdata=df_counts_sum["vote_counts"],
                marker_color="rgb(0, 200, 200)",
                hovertemplate="<b>Nay Votes</b><br><br>"
                + "Referendum id: %{x:.0f}<br>"
                + "Nay Vote counts: %{y:.0f}<br>"
                + "Total counts: %{customdata:.0f}<br>"
                + "<extra></extra>",
            ),
        ]
    if selected_toggle_value == True:
        first_graph_data = [
            go.Bar(
                name="Total Votes",
                x=df_counts_sum["referendum_index"],
                y=df_counts_sum["vote_counts"],
                customdata=df_counts_sum["duration"],
                marker=dict(
                    color=df_counts_sum[
                        "duration"
                    ],  # set color equal to a variable # one of plotly colorscales
                    colorscale="earth",
                    showscale=True,
                ),
                hovertemplate="<b>Delegated Votes</b><br><br>"
                + "Referendum id: %{x:.0f}<br>"
                + "Votes counts: %{y:.0f}<br>"
                + "Duration: %{customdata:.1f} days<br>"
                + "<extra></extra>",
            ),
        ]
    fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
    return fig_first_graph


# Update second chart
@app.callback(
    output=Output("turnout_scatterchart", "figure"),
    inputs=[Input("turn_out_chart_selection", "value")],
    state=[Input("referenda-data", "data"), Input("selected-ids", "value")],
)
def update_bar_chart(selected_toggle_value, referenda_data, selected_ids):
    df_referendum = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referendum = df_referendum[
            (df_referendum["referendum_index"] >= selected_ids[0])
            & (df_referendum["referendum_index"] <= selected_ids[1])
        ]
    if selected_toggle_value == False:
        second_graph_data = [
            go.Scatter(
                name="Aye Votes",
                x=df_referendum["referendum_index"],
                y=df_referendum["aye_amount"],
                fill="tozeroy",
                customdata=df_referendum["turnout"],
                stackgroup="one",  # define stack group
                hovertemplate="<b>Aye Votes</b><br><br>"
                + "Referendum id: %{x:.0f}<br>"
                + "Aye amount: %{y:.0f}<br>"
                + "Turnout: %{customdata:.0f}<br>"
                + "<extra></extra>",
            ),
            go.Scatter(
                name="Nay Votes",
                x=df_referendum["referendum_index"],
                y=df_referendum["nay_amount"],
                customdata=df_referendum["turnout"],
                fill="tonexty",
                stackgroup="one",  # define stack group
                hovertemplate="<b>Nay Votes</b><br><br>"
                + "Referendum id: %{x:.0f}<br>"
                + "Nay Amount: %{y:.0f}<br>"
                + "Turnout: %{customdata:.0f}<br>"
                + "<extra></extra>",
            ),
        ]
    if selected_toggle_value == True:
        second_graph_data = [
            go.Bar(
                name="Aye Votes",
                x=df_referendum["referendum_index"],
                y=df_referendum["aye_turnout_perc"],
                marker_color="rgb(0, 0, 100)",
                customdata=df_referendum["turnout_perc"],
                hovertemplate="<b>Aye Votes</b><br><br>"
                + "Referendum id: %{x:.1f}<br>"
                + "Turnout perc - aye: %{y:.1f}<br>"
                + "Turnout perc: %{customdata:.1f}<br>"
                + "<extra></extra>",
            ),
            go.Bar(
                name="Nay Votes",
                x=df_referendum["referendum_index"],
                y=df_referendum["nay_turnout_perc"],
                customdata=df_referendum["turnout_perc"],
                marker_color="rgb(0, 200, 200)",
                hovertemplate="<b>Nay Votes</b><br><br>"
                + "Referendum id: %{x:.1f}<br>"
                + "Turnout perc - nay: %{y:.1f}<br>"
                + "Turnout perc: %{customdata:.1f}<br>"
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
    )
    fig_second_graph = go.Figure(data=second_graph_data, layout=second_graph_layout)
    return fig_second_graph


# Update third chart
@app.callback(
    Output("new_accounts_barchart", "figure"),
    [
        Input("referenda-data", "data"),
        Input("votes-data", "data"),
        Input("selected-ids", "value"),
    ],
)
def update_new_accounts_chart(referenda_data, votes_data, selected_ids):
    df_new_accounts = get_df_new_accounts(referenda_data, votes_data)
    if selected_ids:
        df_new_accounts = df_new_accounts[
            (df_new_accounts["referendum_index"] >= selected_ids[0])
            & (df_new_accounts["referendum_index"] <= selected_ids[1])
        ]
    third_graph_data = [
        go.Bar(
            name="New accounts counts",
            x=df_new_accounts["referendum_index"],
            y=df_new_accounts["new_accounts"],
            marker_color="rgb(0, 200, 200)",
            hovertemplate="Referendum id: %{x:.0f}<br>"
            + "New accounts counts: %{y:.0f}<br>"
            + "<extra></extra>",
        ),
        go.Scatter(
            name="% of total votes counts",
            x=df_new_accounts["referendum_index"],
            y=df_new_accounts["perc_new_accounts"],
            # mode="lines+markers",
            yaxis="y2",
            line=dict(color="rgb(0, 0, 100)"),
            # marker=dict(color="rgb(0, 0, 100)", size=4),
            hovertemplate="Referendum id: %{x:.0f}<br>"
            + "% of total votes counts: %{y:.4f}<br>"
            + "<extra></extra>",
        ),
    ]

    third_graph_layout = go.Layout(
        title="<b>New accounts for selected Referendum IDs</b>",
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="New accounts counts", linecolor="#021C1E"),
        yaxis2=dict(
            title="New accounts counts (% of total votes counts)",
            linecolor="#021C1E",
            anchor="x",
            overlaying="y",
            side="right",
        ),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )

    fig_third_graph = go.Figure(data=third_graph_data, layout=third_graph_layout)
    return fig_third_graph


# Update forth chart
@app.callback(
    Output("voted_ksm_scatterchart", "figure"),
    [Input("votes-data", "data"), Input("selected-ids", "value")],
)
def update_vote_amount_with_conviction_chart(votes_data, selected_ids):
    df_votes = pd.DataFrame(votes_data)
    if selected_ids:
        df_votes = df_votes[
            (df_votes["referendum_index"] >= selected_ids[0])
            & (df_votes["referendum_index"] <= selected_ids[1])
        ]
    df_vote_amount_with_conviction_mean = (
        df_votes[["referendum_index", "vote_amount_with_conviction"]]
        .groupby("referendum_index")
        .mean()
    )
    df_vote_amount_with_conviction_median = (
        df_votes[["referendum_index", "vote_amount_with_conviction"]]
        .groupby("referendum_index")
        .median()
    )
    forth_graph_data = [
        go.Scatter(
            name="mean",
            x=df_vote_amount_with_conviction_mean.index,
            y=df_vote_amount_with_conviction_mean["vote_amount_with_conviction"],
            mode="lines+markers",
            line=dict(color="rgb(0, 0, 100)", dash="dot"),
            marker=dict(color="rgb(0, 0, 100)", size=4),
            hovertemplate="Referendum index: %{x:.0f}<br>"
            + "vote amount with conviction mean: %{y:.4f}<br>"
            + "<extra></extra>",
        ),
        go.Scatter(
            name="median",
            x=df_vote_amount_with_conviction_median.index,
            y=df_vote_amount_with_conviction_median["vote_amount_with_conviction"],
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="rgb(0, 200, 200)", dash="dash"),
            marker=dict(color="rgb(0, 200, 200)", size=6),
            hovertemplate="Referendum index: %{x:.0f}<br>"
            + "vote amount with conviction median: %{y:.4f}<br>"
            + "<extra></extra>",
        ),
    ]
    forth_graph_layout = go.Layout(
        title="<b>Locked KSM Mean and Median for selected Referendum IDs</b>",
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Vote Amount with Conviction - Mean", linecolor="#021C1E"),
        yaxis2=dict(
            title="Vote Amount with Conviction - Median",
            linecolor="#021C1E",
            anchor="x",
            overlaying="y",
            side="right",
        ),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )
    fig_forth_graph = go.Figure(data=forth_graph_data, layout=forth_graph_layout)
    return fig_forth_graph


# Update piechart
@app.callback(
    Output("call_module_piechart", "figure"),
    [Input("referenda-data", "data"), Input("selected-ids", "value")],
)
def update_pie_chart(referenda_data, selected_ids):
    df = pd.DataFrame(referenda_data)
    if selected_ids:
        df = df[
            (df["referendum_index"] >= selected_ids[0])
            & (df["referendum_index"] <= selected_ids[1])
        ]
    new_figure = {
        "data": [
            {
                "labels": df["call_module"].value_counts().index.tolist(),
                "values": list(df["call_module"].value_counts()),
                "type": "pie",
                "marker": {"li": dict(color="white", width=2)},
                "hoverinfo": "label",
                "textinfo": "label",
            }
        ],
        "layout": {
            "margin": dict(t=20, b=50),
            "uirevision": True,
            "font": {"color": "white"},
            "showlegend": False,
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "autosize": True,
        },
    }
    return new_figure
