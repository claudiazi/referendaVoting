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

# from utils.data_preparation import filter_referenda
from utils.plotting import blank_figure
from config import default_ids_range_dict, filters_gov2


def filter_referenda(
    df_referenda: pd.DataFrame,
    selected_ids,
    cross_filters_input_list,
    cross_filters_list,
) -> pd.DataFrame:
    print(cross_filters_input_list)
    if selected_ids:
        df_referenda = df_referenda[
            (df_referenda["referendum_index"] >= selected_ids[0])
            & (df_referenda["referendum_index"] <= selected_ids[1])
        ]
    for filter_input, filter in zip(cross_filters_input_list, cross_filters_list):
        if filter_input != None and filter_input != "All":
            df_referenda = df_referenda[df_referenda[filter] == filter_input]
    return df_referenda


def create_cross_filters(filters_list, gov_version):
    dcc_list = []
    for filter in filters_list:
        dcc_list.append(
            dcc.Dropdown(
                id=f"crossfilter_{filter}_{gov_version}",
                searchable=True,
                style={
                    "width": "90%",
                    "margin": 0,
                    "padding": 0,
                    "border": 0,
                },
                className="three columns",
            )
        )
    return dcc_list


def build_gov2_tab_1():
    return [
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(className="section-banner", children="Ongoing Referenda"),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            className="twelve columns",
            children=[
                dcc.Loading(
                    html.Div(
                        id="live-data-table-gov2",
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
                    id="id-rangebar-gov2",
                    className="twelve columns",
                    children=[
                        "Loading",
                        dcc.RangeSlider(
                            id="selected-ids-gov2", min=0, max=20, marks=None
                        ),
                    ],
                ),
                html.Div([], className="one column"),
            ]
        ),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            id="cross-filters-gov2",
            children=create_cross_filters(
                filters_list=filters_gov2, gov_version="gov2"
            ),
            className="twelve columns",
            style={"display": "inline-block", "align": "center"},
        ),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            className="twelve columns",
            children=[
                html.Div(html.Br(), className="five columns"),
                html.Button(
                    "Clear Selection",
                    id="clear-radio-gov2",
                    className="click-button",
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
                                    id="votes_counts_chart_selection_gov2",
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
                                                id="votes_counts_barchart_gov2",
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
                                    id="turn_out_chart_selection_gov2",
                                    className="toggle_switch",
                                    label=["Voted amount", "Turnout"],
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
                                                id="turnout_scatterchart_gov2",
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
                                    id="new_accounts_selection_gov2",
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
                                                id="new_accounts_barchart_gov2",
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
                                    id="conviction_selection_gov2",
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
                                                id="voted_ksm_scatterchart_gov2",
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
                                    id="delegated_chart_selection_gov2",
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
                                                id="delegation_barchart_gov2",
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
                                    id="voter_type_chart_selection_gov2",
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
                                                id="voter_type_barchart_gov2",
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
                                    id="voting_time_selection_gov2",
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
                                                id="voting_time_barchart_gov2",
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
                            id="sixth-chart-gov2",
                            className="twelve columns",
                            children=[
                                html.Div(
                                    className="twelve columns", children=[html.Br()]
                                ),
                                html.Div(
                                    id="fifth-chart-gov2",
                                    className="twelve columns",
                                    children=[
                                        dcc.Loading(
                                            id="loading-icon",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="vote_timing_distribution_gov2",
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
            className="twelve columns",
            children=[
                html.Div(
                    id="section-piechart-gov2",
                    className="six columns graph-block",
                    children=[
                        dcc.Loading(
                            id="loading-icon",
                            children=[
                                html.Div(
                                    dcc.Graph(
                                        id="section_piechart_gov2",
                                        figure=blank_figure(),
                                    )
                                )
                            ],
                            type="default",
                        )
                    ],
                ),
                html.Div(
                    id="method-piechart-gov2",
                    className="six columns graph-block",
                    children=[
                        dcc.Loading(
                            id="loading-icon",
                            children=[
                                html.Div(
                                    dcc.Graph(
                                        id="method_piechart_gov2",
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
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            className="twelve columns",
            children=[
                html.Div(
                    className="six columns graph-block",
                    children=[
                        html.Div(
                            id="fifth-chart-gov2",
                            className="twelve columns",
                            children=[
                                dcc.Loading(
                                    id="loading-icon",
                                    children=[
                                        html.Div(
                                            dcc.Graph(
                                                id="submission_deposit_who_piechart_gov2",
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
                                    id="quiz_selection_gov2",
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
                                                id="quiz_answers_barchart_gov2",
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
    ]


layout = build_gov2_tab_1()


@app.callback(
    Output("id-rangebar-gov2", "children"),
    [Input("full-referenda-data", "data"), Input("gov_version", "value")],
)
def create_rangeslider(full_referenda_data, gov_version):
    df = pd.DataFrame(full_referenda_data)
    range_min = df["referendum_index"].min()
    range_max = df["referendum_index"].max()
    return dcc.RangeSlider(
        id="selected-ids-gov2",
        min=range_min,
        max=range_max,
        value=[default_ids_range_dict[gov_version], range_max],
        tooltip={"placement": "top", "always_visible": True},
    )


@app.callback(
    Output("cross-filters-gov2", "children"),
    Input("full-referenda-data", "data"),
)
def create_cross_filters(full_referenda_data):
    df = pd.DataFrame(full_referenda_data)
    filters = [html.Div("Filters", className="two columns")]
    for filter in filters_gov2:
        filter_values = list(df[filter].unique())
        filters.append(
            html.Div(
                children=[
                    dcc.Dropdown(
                        options=filter_values,
                        id=f"crossfilter_{filter}_gov2",
                        searchable=True,
                        style={
                            "width": "90%",
                            "margin": 0,
                            "padding": 0,
                            "border": 0,
                        },
                        className="three columns",
                        placeholder=filter,
                    )
                ]
            )
        )
    return filters


@app.callback(
    Output("live-data-table-gov2", "children"),
    [Input("ongoing-referenda-data", "data")],
)
def create_live_data_table(ongoing_referenda_data):
    df = pd.DataFrame(ongoing_referenda_data)
    print(f"live data updated {time.time()}")
    df["voted_amount_with_conviction_aye_perc"] = (
        df["voted_amount_with_conviction_aye"]
        / df["voted_amount_with_conviction_total"]
        * 100
    )
    df["voted_amount_with_conviction_nay_perc"] = (
        df["voted_amount_with_conviction_nay"]
        / df["voted_amount_with_conviction_total"]
        * 100
    )
    df["turnout_total_perc"] = df["turnout_total_perc"].apply(lambda x: f"{x:.2f} %")
    df["voted_amount_with_conviction_aye"] = df.apply(
        lambda x: f"{x['voted_amount_with_conviction_aye']:.2f} ({x['voted_amount_with_conviction_aye_perc']:.2f} %)",
        axis=1,
    )
    df["voted_amount_with_conviction_nay"] = df.apply(
        lambda x: f"{x['voted_amount_with_conviction_nay']:.2f} ({x['voted_amount_with_conviction_nay_perc']:.2f} %)",
        axis=1,
    )
    df = df[
        [
            "referendum_index",
            "section",
            "turnout_total_perc",
            "voted_amount_with_conviction_aye",
            "voted_amount_with_conviction_nay",
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


# Update first chart
@app.callback(
    output=Output("votes_counts_barchart_gov2", "figure"),
    inputs=[
        Input("interval-component", "n_intervals"),
        Input("selected-ids-gov2", "value"),
        Input("votes_counts_chart_selection_gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
    state=Input("full-referenda-data", "data"),
)
def update_votes_counts_chart(
    n_intervals,
    selected_ids,
    selected_toggle_value,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
    referenda_data,
):
    df_referenda = pd.DataFrame(referenda_data).sort_values(by="referendum_index")
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
    first_graph_layout = go.Layout(
        title="<b>Vote Count</b>",
        barmode="stack",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Vote counts", linecolor="#021C1E"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
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


@app.callback(
    output=Output("turnout_scatterchart_gov2", "figure"),
    inputs=[
        Input("turn_out_chart_selection_gov2", "value"),
        Input("full-referenda-data", "data"),
        Input("selected-ids-gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
)
def update_bar_chart(
    selected_toggle_value,
    referenda_data,
    selected_ids,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
):
    df_referenda = pd.DataFrame(referenda_data)
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
    if selected_toggle_value == False:
        second_graph_data = [
            go.Scatter(
                name="Aye Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["voted_amount_with_conviction_aye"],
                marker_color="#ffffff",
                fill="tozeroy",
                customdata=df_referenda["voted_amount_with_conviction_total"],
                stackgroup="one",  # define stack group
                hovertemplate="<b>Aye Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Aye amount with conviction: %{y:.1f}<br>"
                + "Turnout: %{customdata:.2f}<br>"
                + "<extra></extra>",
            ),
            go.Scatter(
                name="Nay Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["voted_amount_with_conviction_nay"],
                customdata=df_referenda["voted_amount_with_conviction_total"],
                marker_color="#e6007a",
                fill="tonexty",
                stackgroup="one",  # define stack group
                hovertemplate="<b>Nay Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Nay Amount with conviction: %{y:.1f}<br>"
                + "Turnout: %{customdata:.2f}<br>"
                + "<extra></extra>",
            ),
        ]
        title = "Voted Amount"
        yaxis_name = "Voted Amount"
    else:
        second_graph_data = [
            go.Bar(
                name="Aye Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["turnout_aye_perc"],
                marker_color="#ffffff",
                opacity=0.8,
                customdata=df_referenda["voted_amount_aye"],
                hovertemplate="<b>Aye Votes</b><br><br>"
                + "Referendum id: %{x:.0f}<br>"
                + "Turnout - aye: %{y:.2f} %<br>"
                + "Voted amount without conviction - aye: %{customdata:.2f}<br>"
                + "<extra></extra>",
            ),
            go.Bar(
                name="Nay Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["turnout_nay_perc"],
                opacity=0.8,
                customdata=df_referenda["voted_amount_nay"],
                marker_color="#e6007a",
                hovertemplate="<b>Nay Votes</b><br><br>"
                + "Referendum id: %{x:.0f}<br>"
                + "Turnout - nay: %{y:.2f} %<br>"
                + "Voted amount without conviction - nay: %{customdata:.2f}<br>"
                + "<extra></extra>",
            ),
        ]
        title = "Turnout"
        yaxis_name = "Turnout (% of total issued Kusama)"

    second_graph_layout = go.Layout(
        title=f"<b>{title}</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title=yaxis_name, linecolor="#021C1E"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
        template="plotly_dark",
        hovermode="x",
    )
    fig_second_graph = go.Figure(data=second_graph_data, layout=second_graph_layout)
    return fig_second_graph


@app.callback(
    output=Output("new_accounts_barchart_gov2", "figure"),
    inputs=[Input("new_accounts_selection_gov2", "value")],
    state=[
        Input("full-referenda-data", "data"),
        Input("selected-ids-gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
)
def update_new_accounts_chart(
    selected_toggle_value,
    referenda_data,
    selected_ids,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
):
    df_referenda = pd.DataFrame(referenda_data)
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
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
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
        template="plotly_dark",
    )

    fig_third_graph = go.Figure(data=third_graph_data, layout=third_graph_layout)
    return fig_third_graph


# Update forth chart
@app.callback(
    output=Output("voted_ksm_scatterchart_gov2", "figure"),
    inputs=[Input("conviction_selection_gov2", "value")],
    state=[
        Input("full-referenda-data", "data"),
        Input("selected-ids-gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
)
def update_vote_amount_with_conviction_chart(
    selected_toggle_value,
    referenda_data,
    selected_ids,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
):
    df_referenda = pd.DataFrame(referenda_data)
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
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
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
    )
    fig_forth_graph = go.Figure(data=forth_graph_data, layout=forth_graph_layout)
    return fig_forth_graph


@app.callback(
    output=Output("delegation_barchart_gov2", "figure"),
    inputs=[Input("delegated_chart_selection_gov2", "value")],
    state=[
        Input("full-referenda-data", "data"),
        Input("selected-ids-gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
)
def update_delegation_chart(
    selected_toggle_value,
    referenda_data,
    selected_ids,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
):
    df_referenda = pd.DataFrame(referenda_data)
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
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
                y=df_referenda["voted_amount_with_conviction_direct"],
                marker_color="#ffffff",
                fill="tozeroy",
                stackgroup="one",  # define stack group
                customdata=df_referenda["voted_amount_with_conviction_total"],
                hovertemplate="<b>Direct Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Voted amount - Direct: %{y:.0f}<br>"
                + "Voted amount - Total: %{customdata:.0f}<br>"
                + "<extra></extra>",
            ),
            go.Scatter(
                name="Delegated Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["voted_amount_with_conviction_delegated"],
                customdata=df_referenda["voted_amount_with_conviction_total"],
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
        title="<b>Delegated vs Direct</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title=yaxis_name, linecolor="#021C1E"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
        template="plotly_dark",
        hovermode="x",
    )
    fig_v_graph = go.Figure(data=v_graph_data, layout=v_graph_layout)
    return fig_v_graph


@app.callback(
    output=Output("voter_type_barchart_gov2", "figure"),
    inputs=[Input("voter_type_chart_selection_gov2", "value")],
    state=[
        Input("full-referenda-data", "data"),
        Input("selected-ids-gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
)
def update_voter_type_chart(
    selected_toggle_value,
    referenda_data,
    selected_ids,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
):
    df_referenda = pd.DataFrame(referenda_data)
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
    if selected_toggle_value == False:
        v_graph_data = [
            go.Bar(
                name="Validator Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_validator"],
                marker_color="#e6007a",
                customdata=df_referenda["count_total"],
                hovertemplate="<b>Validator Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Count validator votes: %{y:.0f}<br>"
                + "Count total: %{customdata:.0f}<br>"
                + "<extra></extra>",
                opacity=0.8,
            ),
            go.Bar(
                name="Normal Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_normal"],
                customdata=df_referenda["count_total"],
                marker_color="#ffffff",
                hovertemplate="<b>Normal Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Count normal votes: %{y:.0f}<br>"
                + "Count total: %{customdata:.0f}<br>"
                + "<extra></extra>",
                opacity=0.8,
            ),
        ]
        yaxis_name = "Vote Count"
    else:
        v_graph_data = [
            go.Bar(
                name="Validator Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["voted_amount_with_conviction_validator"],
                marker_color="#e6007a",
                customdata=df_referenda["voted_amount_with_conviction_total"],
                hovertemplate="<b>Validator Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Voted amount - validator: %{y:.0f}<br>"
                + "Voted amount - total: %{customdata:.0f}<br>"
                + "<extra></extra>",
                opacity=0.8,
            ),
            go.Bar(
                name="Normal Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["voted_amount_with_conviction_normal"],
                customdata=df_referenda["voted_amount_with_conviction_total"],
                marker_color="#ffffff",
                hovertemplate="<b>Normal Votes</b><br><br>"
                + "Referendum: %{x:.0f}<br>"
                + "Voted amount - normal: %{y:.0f}<br>"
                + "Voted amount - total: %{customdata:.0f}<br>"
                + "<extra></extra>",
                opacity=0.8,
            ),
        ]
        yaxis_name = "Voted Amount"

    v_graph_layout = go.Layout(
        title="<b>Voter Type</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title=yaxis_name, linecolor="#021C1E"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
        template="plotly_dark",
        hovermode="x",
    )
    fig_v_graph = go.Figure(data=v_graph_data, layout=v_graph_layout)
    return fig_v_graph


@app.callback(
    output=Output("voting_time_barchart_gov2", "figure"),
    inputs=[Input("voting_time_selection_gov2", "value")],
    state=[
        Input("full-referenda-data", "data"),
        Input("selected-ids-gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
)
def update_voting_time_barchart(
    selected_toggle_value,
    referenda_data,
    selected_ids,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
):
    df_referenda = pd.DataFrame(referenda_data)
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
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
                )
            )
        fifth_graph_layout = go.Layout(
            title="<b>When Wallets Voted</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Count of voting time groups", linecolor="#021C1E"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="left", x=0),
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


@app.callback(
    output=Output("vote_timing_distribution_gov2", "figure"),
    inputs=[
        Input("full-referenda-data", "data"),
        Input("selected-ids-gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
)
def update_vote_timing_distribution(
    referenda_data,
    selected_ids,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
):
    df_referenda = pd.DataFrame(referenda_data)
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
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


@app.callback(
    Output("section_piechart_gov2", "figure"),
    [
        Input("full-referenda-data", "data"),
        Input("selected-ids-gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
)
def update_section_pie_chart(
    referenda_data,
    selected_ids,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
):
    df_referenda = pd.DataFrame(referenda_data)
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
    df_section_group_count = df_referenda["section"].value_counts()
    ix_graph_data = [
        go.Pie(
            labels=df_section_group_count.index,
            values=df_section_group_count.values,
            marker=dict(colors=color_scale),
            textposition="inside",
            opacity=0.8,
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
        uniformtext_minsize=6,
        uniformtext_mode="hide",
    )
    fig_ix_graph = go.Figure(data=ix_graph_data, layout=ix_graph_layout)
    return fig_ix_graph


@app.callback(
    Output("method_piechart_gov2", "figure"),
    [
        Input("full-referenda-data", "data"),
        Input("selected-ids-gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
)
def update_method_pie_chart(
    referenda_data,
    selected_ids,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
):
    df_referenda = pd.DataFrame(referenda_data)
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
    df_method_group_count = (
        df_referenda.groupby("method")
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
    )
    df_method_group_count["method_short"] = df_method_group_count["method"].apply(
        lambda x: f"{x[:20]}..."
    )
    x_graph_data = [
        go.Pie(
            labels=df_method_group_count["method_short"],
            values=df_method_group_count["count"],
            marker=dict(colors=color_scale),
            textposition="inside",
            opacity=0.8,
            customdata=df_method_group_count["method"],
            hovertemplate="%{customdata}<br>" + "%{percent}" + "<extra></extra>",
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
        uniformtext_minsize=6,
        uniformtext_mode="hide",
    )
    fig_x_graph = go.Figure(data=x_graph_data, layout=x_graph_layout)
    return fig_x_graph


@app.callback(
    Output("submission_deposit_who_piechart_gov2", "figure"),
    [
        Input("full-referenda-data", "data"),
        Input("selected-ids-gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
)
def update_submission_pie_chart(
    referenda_data,
    selected_ids,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
):
    df_referenda = pd.DataFrame(referenda_data)
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
    df_proposer_count = (
        df_referenda.groupby("submission_deposit_who")
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
    )
    df_proposer_count["proposer_short"] = df_proposer_count[
        "submission_deposit_who"
    ].apply(lambda x: f"{x[:6]}...{x[-4:]}")
    xi_graph_data = [
        go.Pie(
            labels=df_proposer_count["proposer_short"],
            values=df_proposer_count["count"],
            marker=dict(colors=color_scale),
            customdata=df_proposer_count["submission_deposit_who"],
            textposition="inside",
            hovertemplate="%{customdata}<br>" + "%{percent}" + "<extra></extra>",
        )
    ]
    xi_graph_layout = go.Layout(
        title="<b>Submission Deposit Who</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.8),
        template="plotly_dark",
        hovermode="x",
        autosize=True,
        clickmode="event+select",
        uniformtext_minsize=6,
        uniformtext_mode="hide",
    )
    fig_xi_graph = go.Figure(data=xi_graph_data, layout=xi_graph_layout)
    return fig_xi_graph


@app.callback(
    output=Output("quiz_answers_barchart_gov2", "figure"),
    inputs=[Input("quiz_selection_gov2", "value")],
    state=[
        Input("full-referenda-data", "data"),
        Input("selected-ids-gov2", "value"),
        Input("crossfilter_section_gov2", "value"),
        Input("crossfilter_method_gov2", "value"),
        Input("crossfilter_submission_deposit_who_gov2", "value"),
        Input("crossfilter_decision_deposit_who_gov2", "value"),
    ],
)
def update_quiz_answer_chart(
    selected_toggle_value,
    referenda_data,
    selected_ids,
    selected_section,
    selected_method,
    selected_submission_deposit_who,
    selected_decision_deposit_who,
):
    df_referenda = pd.DataFrame(referenda_data)
    filters_input = [
        selected_section,
        selected_method,
        selected_submission_deposit_who,
        selected_decision_deposit_who,
    ]
    df_referenda = filter_referenda(
        df_referenda, selected_ids, filters_input, filters_gov2
    )
    df_referenda = df_referenda[df_referenda["count_quiz_attended_wallets"].notnull()]
    if selected_toggle_value == False:
        xii_graph_data = [
            go.Bar(
                name="# Quiz Attended",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_quiz_attended_wallets"],
                marker_color="#e6007a",
                opacity=0.8,
                hovertemplate="Referendum: %{x:.0f}<br>"
                + "# quiz attended: %{y:.0f}<br>"
                + "<extra></extra>",
            ),
            go.Scatter(
                name="Fully Correct Answers",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_fully_correct"],
                marker_color="#ffffff",
                opacity=0.8,
                mode="lines+markers",
                hovertemplate="Referendum: %{x:.0f}<br>"
                + "Fully correct wallets: %{y:.0f}<br>"
                + "<extra></extra>",
            ),
        ]
        yaxis_name = "Count"
    else:
        xii_graph_data = [
            go.Scatter(
                name="% Attendants of Total Votes",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_quiz_attended_wallets"]
                / df_referenda["count_total"]
                * 100,
                mode="lines+markers",
                line=dict(color="#e6007a"),
                opacity=0.8,
                # marker=dict(color="rgb(0, 0, 100)", size=4),
                hovertemplate="Referendum: %{x:.0f}<br>"
                + "% of total answers: %{y:.4f}<br>"
                + "<extra></extra>",
            ),
            go.Scatter(
                name="% fully correct of Total Answers",
                x=df_referenda["referendum_index"],
                y=df_referenda["count_fully_correct"]
                / df_referenda["count_quiz_attended_wallets"]
                * 100,
                mode="lines+markers",
                line=dict(color="#ffffff"),
                opacity=0.8,
                # marker=dict(color="rgb(0, 0, 100)", size=4),
                hovertemplate="Referendum: %{x:.0f}<br>"
                + "% of total answers: %{y:.4f}<br>"
                + "<extra></extra>",
            ),
        ]
        yaxis_name = "% of Total Answers"
    xii_graph_layout = go.Layout(
        title="<b>Quiz attendants</b>",
        paper_bgcolor="#161a28",
        plot_bgcolor="#161a28",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title=yaxis_name, linecolor="#021C1E"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
        template="plotly_dark",
    )

    fig_xii_graph = go.Figure(data=xii_graph_data, layout=xii_graph_layout)
    return fig_xii_graph


@app.callback(
    [
        Output("crossfilter_section_gov2", "value"),
        Output("crossfilter_method_gov2", "value"),
        Output("crossfilter_proposer_gov2", "value"),
    ],
    [Input("clear-radio", "n_clicks")],
)
def clear_section_selections(*args):
    return None, None, None
