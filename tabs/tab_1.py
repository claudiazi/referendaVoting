import time

import dash_daq as daq
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from config import voting_group_dict, voting_group_perc_dict, voting_group_colors
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
                    className="six columns graph-block",
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
                    className="six columns graph-block",
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
                    className="six columns graph-block",
                    children=[
                        html.Div(
                            className="twelve columns",
                            children=[
                                daq.ToggleSwitch(
                                    id="conviction_selection",
                                    label=["Median", "Mean"],
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
                                    value=True,
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
                                    className="reset-button",
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
                            id="sixth-chart",
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
    ]


layout = build_tab_1()


@app.callback(
    Output("id-rangebar", "children"),
    [Input("closed-referenda-data", "data")],
)
def create_rangeslider(closed_referenda_data):
    df = pd.DataFrame(closed_referenda_data)
    range_min = df["referendum_index"].min()
    range_max = df["referendum_index"].max()
    return dcc.RangeSlider(id="selected-ids", min=range_min, max=range_max)


@app.callback(
    Output("live-data-table", "children"), Input("ongoing-referenda-data", "data")
)
def create_live_data_table(data):
    dff = pd.DataFrame(data[:])
    print(f"live data updated {time.time()}")
    dff = dff[["referendum_index", "section", "turnout_aye_perc", "voted_amount_total"]]

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
            + data_perc_bars(dff, "turnout_aye_perc")
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


# Update first chart
@app.callback(
    output=Output("votes_counts_barchart", "figure"),
    inputs=[
        Input("interval-component", "n_intervals"),
        Input("selected-ids", "value"),
        Input("votes_counts_chart_selection", "value"),
        Input("section_piechart", "clickData"),
    ],
    state=Input("closed-referenda-data", "data"),
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
                marker_color="rgb(0, 0, 100)",
                customdata=df_referenda["count_total"],
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
                marker_color="#B7B8BB",
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
                customdata=df_referenda["vote_duration"],
                marker=dict(
                    color=df_referenda[
                        "vote_duration"
                    ],  # set color equal to a variable # one of plotly colorscales
                    colorscale="earth",
                    showscale=True,
                ),
                hovertemplate="<b>Referendum</b><br><br>"
                + "Duration: %{customdata:.0f}<br>"
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
    state=[Input("closed-referenda-data", "data"), Input("selected-ids", "value")],
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
                fill="tozeroy",
                customdata=df_referenda["voted_amount_total"],
                stackgroup="one",  # define stack group
                hovertemplate="<b>Aye Votes</b><br><br>"
                + "Referendum id: %{x:.0f}<br>"
                + "Aye amount: %{y:.0f}<br>"
                + "Turnout: %{customdata:.0f}<br>"
                + "<extra></extra>",
            ),
            go.Scatter(
                name="Nay Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["voted_amount_nay"],
                customdata=df_referenda["voted_amount_total"],
                fill="tonexty",
                stackgroup="one",  # define stack group
                hovertemplate="<b>Nay Votes</b><br><br>"
                + "Referendum id: %{x:.0f}<br>"
                + "Nay Amount: %{y:.0f}<br>"
                + "Turnout: %{customdata:.0f}<br>"
                + "<extra></extra>",
            ),
        ]
    else:
        second_graph_data = [
            go.Bar(
                name="Aye Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["turnout_aye_perc"],
                marker_color="rgb(0, 0, 100)",
                customdata=df_referenda["turnout_total_perc"],
                hovertemplate="<b>Aye Votes</b><br><br>"
                + "Referendum id: %{x:.1f}<br>"
                + "Turnout perc - aye: %{y:.1f}<br>"
                + "Turnout perc: %{customdata:.1f}<br>"
                + "<extra></extra>",
            ),
            go.Bar(
                name="Nay Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["turnout_nay_perc"],
                customdata=df_referenda["turnout_total_perc"],
                marker_color="rgb(0, 200, 200)",
                hovertemplate="<b>Nay Votes</b><br><br>"
                + "Referendum id: %{x:.2f}<br>"
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
        Input("closed-referenda-data", "data"),
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
    state=[Input("closed-referenda-data", "data"), Input("selected-ids", "value")],
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
                hovertemplate="Referendum index: %{x:.0f}<br>"
                + "vote amount with conviction mean: %{y:.4f}<br>"
                + "<extra></extra>",
            ),
        ]
        forth_graph_layout = go.Layout(
            title="<b>Locked KSM Mean and Median for selected Referendum IDs</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            template="plotly_dark",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(
                title="Vote Amount with Conviction - Median", linecolor="#021C1E"
            ),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        )
    else:
        forth_graph_data = [
            go.Scatter(
                name="median",
                x=df_referenda["referendum_index"],
                y=df_referenda["conviction_median"],
                mode="lines+markers",
                line=dict(color="#e6007a"),
                marker=dict(color="#e6007a", size=4),
                hovertemplate="Referendum index: %{x:.0f}<br>"
                + "vote amount with conviction median: %{y:.4f}<br>"
                + "<extra></extra>",
            ),
        ]
        forth_graph_layout = go.Layout(
            title="<b>Locked KSM Mean and Median for selected Referendum IDs</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            template="plotly_dark",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(
                title="Vote Amount with Conviction - Meean", linecolor="#021C1E"
            ),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        )
    fig_forth_graph = go.Figure(data=forth_graph_data, layout=forth_graph_layout)
    return fig_forth_graph


# Update fifth chart
@app.callback(
    output=Output("voting_time_barchart", "figure"),
    inputs=[Input("voting_time_selection", "value")],
    state=[Input("closed-referenda-data", "data"), Input("selected-ids", "value")],
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
    state=[Input("closed-referenda-data", "data"), Input("selected-ids", "value")],
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
# Update seventh chart
@app.callback(
    Output("section_piechart", "figure"),
    [Input("closed-referenda-data", "data"), Input("selected-ids", "value")],
)
def update_pie_chart(referenda_data, selected_ids):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    df_section_group_count = df_referenda["section"].value_counts()
    seventh_graph_data = [
        go.Pie(
            labels=df_section_group_count.index,
            values=df_section_group_count.values,
            marker=dict(colors=voting_group_colors),
            textposition="inside",
            # hovertemplate="Referendum id: %{x:.0f}<br>"
            # + "Group count: %{y:.0f}<br>"
            # + "Total: %{customdata:.0f}<br>"
            # + "<extra></extra>",
        )
    ]
    seventh_graph_layout = go.Layout(
        title="<b>Section</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
        template="plotly_dark",
        hovermode="x",
        autosize=True,
        clickmode="event+select",
    )
    fig_seventh_graph = go.Figure(data=seventh_graph_data, layout=seventh_graph_layout)
    return fig_seventh_graph


# Update eighth chart
@app.callback(
    Output("method_piechart", "figure"),
    [
        Input("closed-referenda-data", "data"),
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
    eighth_graph_data = [
        go.Pie(
            labels=df_method_group_count.index,
            values=df_method_group_count.values,
            marker=dict(colors=voting_group_colors),
            textposition="inside",
            # hovertemplate="Referendum id: %{x:.0f}<br>"
            # + "Group count: %{y:.0f}<br>"
            # + "Total: %{customdata:.0f}<br>"
            # + "<extra></extra>",
        )
    ]
    eighth_graph_layout = go.Layout(
        title="<b>Method</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
        template="plotly_dark",
        hovermode="x",
        autosize=True,
        clickmode="event+select",
    )
    fig_eighth_graph = go.Figure(data=eighth_graph_data, layout=eighth_graph_layout)
    return fig_eighth_graph


# Update ninth chart
@app.callback(
    Output("proposer_piechart", "figure"),
    [
        Input("closed-referenda-data", "data"),
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
    ninth_graph_data = [
        go.Pie(
            labels=df_proposer_count.index,
            values=df_proposer_count.values,
            marker=dict(colors=voting_group_colors),
            textposition="inside",
            # hovertemplate="Referendum id: %{x:.0f}<br>"
            # + "Group count: %{y:.0f}<br>"
            # + "Total: %{customdata:.0f}<br>"
            # + "<extra></extra>",
        )
    ]
    ninth_graph_layout = go.Layout(
        title="<b>Proposer</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
        template="plotly_dark",
        hovermode="x",
        autosize=True,
        clickmode="event+select",
    )
    fig_ninth_graph = go.Figure(data=ninth_graph_data, layout=ninth_graph_layout)
    return fig_ninth_graph


# Update tenth chart
@app.callback(
    Output("threshold_piechart", "figure"),
    [
        Input("closed-referenda-data", "data"),
        Input("selected-ids", "value"),
    ],
)
def update_threshold_piechart(referenda_data, selected_ids):
    df_referenda = pd.DataFrame(referenda_data)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])]
    df_threshold_count = df_referenda["threshold_type"].value_counts()
    tenth_graph_data = [
        go.Pie(
            labels=df_threshold_count.index,
            values=df_threshold_count.values,
            marker=dict(colors=voting_group_colors),
            textposition="inside",
            # hovertemplate="Referendum id: %{x:.0f}<br>"
            # + "Group count: %{y:.0f}<br>"
            # + "Total: %{customdata:.0f}<br>"
            # + "<extra></extra>",
        )
    ]
    tenth_graph_layout = go.Layout(
        title="<b>Proposer</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
        template="plotly_dark",
        hovermode="x",
        autosize=True,
        clickmode="event+select",
    )
    fig_tenth_graph = go.Figure(data=tenth_graph_data, layout=tenth_graph_layout)
    return fig_tenth_graph

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

#fig = go.FigureWidget() # create figure widget
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
#     [Input("closed-referenda-data", "data"), Input("selected-ids", "value"), Input("section_piechart", "clickData")],
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
