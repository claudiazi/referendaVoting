import os
import pathlib
import json
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table
import plotly.graph_objs as go
import dash_daq as daq
import numpy as np

import warnings

import pandas as pd
from utils.data_preparation import (
    load_data,
    preprocessing_referendum,
    preprocessing_votes,
)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=external_stylesheets,
)
server = app.server
app.config["suppress_callback_exceptions"] = True

colors = {
    "background": "#111111",
}

mongodb_url = os.getenv("MONGODB_URL")
db_name = os.getenv("DB_NAME")
table_name = os.getenv("TABLE_NAME")

suffix_row = "_row"
suffix_button_id = "_button"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"
suffix_indicator = "_indicator"

theme = {
    "dark": True,
    "detail": "#2d3038",  # Background-card
    "primary": "#007439",  # Green
    "secondary": "#FFD15F",  # Accent
}


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.H1("Kusama Governance Dashboard - Referendum Analysis"),
        ],
    )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Main-tab",
                        label="Main Dashboard",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        disabled_style={
                            "backgroundColor": "#2d3038",
                            "color": "#95969A",
                            "borderColor": "#23262E",
                            "display": "flex",
                            "flex-direction": "column",
                            "alignItems": "center",
                            "justifyContent": "center",
                        },
                        disabled=False,
                    ),
                    dcc.Tab(
                        id="Single-account-tab",
                        label="Single Account View",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        disabled_style={
                            "backgroundColor": "#2d3038",
                            "color": "#95969A",
                            "borderColor": "#23262E",
                            "display": "flex",
                            "flex-direction": "column",
                            "alignItems": "center",
                            "justifyContent": "center",
                        },
                        disabled=False,
                    ),
                ],
            )
        ],
    )


def load_raw_data():
    df_raw = pd.read_csv("test_data.csv")
    print("raw data loaded!")
    return df_raw.to_dict('record')


def load_refined_referenda_data(df_raw):
    # df_raw = load_data(mongodb_url=mongodb_url, db_name=db_name, table_name=table_name)
    df_raw = pd.DataFrame(df_raw)
    df_referendum = preprocessing_referendum(df_raw)
    print('referendum data loaded!')
    return df_referendum.to_dict('record')


def load_refined_votes_data(df_raw):
    # df_raw = load_data(mongodb_url=mongodb_url, db_name=db_name, table_name=table_name)
    df_raw = pd.DataFrame(df_raw)
    df_votes = preprocessing_votes(df_raw)
    print('votes data loaded!')
    return df_votes.to_dict('record')

#
# df_raw = load_raw_data()
# referenda_dict = load_refined_referenda_data(df_raw)
# votes_dict = load_refined_votes_data(df_raw)


def build_tab_1():
    return [
        # rangebar
        html.Div(
            id="selected-ids",
            className="twelve columns",
            children=[
                html.Br(),
                dcc.RangeSlider(65, 217),
            ],
        ),
        html.Div(
            id="settings-menu",
            children=[
                html.Div(
                    id="first-chart",
                    className="six columns",
                    children=[html.Br(), generate_bar_chart()],
                ),
                html.Div(
                    id="second-chart",
                    className="six columns",
                    children=[html.Br(), generate_turnout_chart()],
                ),
                html.Div(
                    id="first-pie-chart",
                    className="five columns",
                    children=[
                        html.Label(id="metric-select-title", children="Select Metrics"),
                        html.Br(),
                        generate_piechart(),
                    ],
                ),
                html.Div(
                    id="table-placeholder",
                    className="five columns",
                    children=[],
                ),
            ],
        ),
    ]


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


def generate_bar_chart():
    return dcc.Graph(
        id="votes_counts_barchart",
        figure={
            "data": [
                {
                    "labels": [],
                    "values": [],
                    "marker": {"line": {"color": "white", "width": 1}},
                    "hoverinfo": "label",
                    "textinfo": "label",
                }
            ],
            "layout": {
                "title": "<b>Vote counts for selected Referendum IDs</b>",
                "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
                "barmode": "stack",
                "xaxis": dict(title="Referendum ID", linecolor="#BCCCDC"),
                "yaxis": dict(title="Vote counts", linecolor="#021C1E"),
                "legend": dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            },
        },
    )


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
    # Second chart

    second_graph_data = go.Scatter(
        name="Turnout",
        mode="lines+markers",
        line=dict(color="rgb(0, 0, 100)"),
        marker=dict(color="rgb(0, 0, 100)", size=8),
        hovertemplate="Referendum id: %{x:.0f}<br>"
        + "Turnout (%): %{y:.4f}<br>"
        + "<extra></extra>",
    )

    second_graph_layout = go.Layout(
        title="<b>Turnout for selected Referendum IDs</b>",
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Turnout (% of total issued Kusama)", linecolor="#021C1E"),
    )
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        fig_second_graph = go.Figure(data=second_graph_data, layout=second_graph_layout)
        st.plotly_chart(fig_second_graph)
        x = (df_votes_balance_perc.id.astype(int),)
        y = (df_votes_balance_perc["perc"],)


app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2000 * 1000,  # in milliseconds
            n_intervals=0,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        # Main app
        html.Button(
            "Confirm",
            id="tab-trigger-btn",
            n_clicks=0,
            style={"display": "inline-block", "float": "right"},
        ),
        dcc.Store(id="raw-data", data=[], storage_type="memory"),
        dcc.Store(
            id="votes-data", data=[], storage_type="memory"
        ),
        dcc.Store(
            id="referenda-data",
            data=[],
            storage_type="memory",
        ),
        dcc.Store(id="n-interval-stage", data=0),
    ],
)


# Callback to update the stream data
@app.callback(Output("raw-data", "data"), Input("interval-component", "n_intervals"))
def update(n_intervals):
    if n_intervals >= 0:
        return load_raw_data()

@app.callback(
    [Output("referenda-data", "data"), Output("votes-data", "data")],
    Input("raw-data", "data")
)
def update_refined_data(raw_data):
    return load_refined_referenda_data(raw_data), load_refined_votes_data(raw_data)


@app.callback(
    Output('table-placeholder', 'children'),
    Input('referenda-data', 'data')
)
def create_graph1(data):
    dff = pd.DataFrame(data[:])
    dff = dff[['referendum_index', 'turnout_perc']]
    # 2. convert string like JSON to pandas dataframe
    # dff = pd.read_json(data, orient='split')
    my_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in dff.columns],
        data=dff.to_dict('records')
    )
    return my_table


@app.callback(
    [Output("app-content", "children"), Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value")],
    [State("n-interval-stage", "data")],
)
def render_tab_content(tab_switch, stopped_interval):
    if tab_switch == "tab1":
        return build_tab_1(), stopped_interval
    return (
        html.Div(
            id="status-container",
            children=[
                html.H3("Tab content 1"),
                dcc.Graph(
                    figure={"data": [{"x": [1, 2, 3], "y": [3, 1, 2], "type": "bar"}]}
                ),
            ],
        ),
        stopped_interval,
    )


# # Update interval
@app.callback(
    Output("n-interval-stage", "data"),
    [Input("app-tabs", "value")],
    [
        State("interval-component", "n_intervals"),
        State("interval-component", "disabled"),
        State("n-interval-stage", "data"),
    ],
)
def update_interval_state(tab_switch, cur_interval, disabled, cur_stage):
    if disabled:
        return cur_interval

    if tab_switch == "tab1":
        return cur_interval
    return cur_stage


# Update first chart
@app.callback(
    output=Output("votes_counts_barchart", "figure"),
    inputs=[Input("interval-component", "n_intervals")],
    state=[Input("votes-data", "data")],
)
def update_bar_chart(n_intervals, votes_data):
    # delegated=False votes
    # df_non_delegated = df_votes[df_votes["isDelegating"] == 'False']
    # df_non_delegated_count_sum = (
    #     df_non_delegated.groupby("referendum_index")["address"]
    #         .count()
    #         .reset_index(name="vote_counts")
    #         .sort_values(by="referendum_index")
    # )
    #
    # # delegated=True votes
    # df_delegated = df_votes[df_votes["isDelegating"] == 'True']
    # df_delegated_count_sum = (
    #     df_delegated.groupby("referendum_index")["address"]
    #         .count()
    #         .reset_index(name="vote_counts")
    #         .sort_values(by="referendum_index")
    # )
    #
    df_votes = pd.DataFrame(votes_data)
    df_counts_sum = (
        df_votes.groupby("referendum_index")["address"]
            .count()
            .reset_index(name="vote_counts")
            .sort_values(by="referendum_index")
    )

#     COLORS_MAPPER = {
#         "Delegated Votes": "rgb(0, 0, 100)",
#         "Non-delegated Votes": "rgb(0, 200, 200)",
#     }
#     #
    first_graph_layout = go.Layout(
        title="<b>Vote counts for selected Referendum IDs</b>",
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Vote counts", linecolor="#021C1E"),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )
    #
    # total_count = np.transpose(
    #     [
    #         df_delegated_count_sum["id"],
    #         df_delegated_count_sum["vote_counts"]
    #         + df_non_delegated_count_sum["vote_counts"],
    #     ]
    # )
    first_graph_data = [
        # go.Bar(
        #     name="Delegated Votes",
        #     x=df_delegated_count_sum["id"],
        #     y=df_delegated_count_sum["vote_counts"],
        #     marker_color="rgb(0, 0, 100)",
        #     customdata=total_count,
        #     hovertemplate="<b>Delegated Votes</b><br><br>"
        #                   + "Referendum id: %{x:.0f}<br>"
        #                   + "Vote counts: %{y:.0f}<br>"
        #                   + "Total counts: %{customdata[1]:.0f}<br>"
        #                   + "<extra></extra>",
        # ),
        # go.Bar(
        #     name="Non-delegated Votes",
        #     x=df_non_delegated_count_sum["id"],
        #     y=df_non_delegated_count_sum["vote_counts"],
        #     customdata=total_count,
        #     marker_color="rgb(0, 200, 200)",
        #     hovertemplate="<b>Non-delegated Votes</b><br><br>"
        #                   + "Referendum id: %{x:.0f}<br>"
        #                   + "Vote counts: %{y:.0f}<br>"
        #                   + "Total counts: %{customdata[1]:.0f}<br>"
        #                   + "<extra></extra>",
        # ),
        go.Bar(
            name="Total Votes",
            x=df_counts_sum["referendum_index"],
            y=df_counts_sum["vote_counts"],
            marker_color="rgb(0, 0, 100)",
            hovertemplate="<b>Delegated Votes</b><br><br>"
                          + "Referendum id: %{x:.0f}<br>"
                          + "Total counts: %{customdata[1]:.0f}<br>"
                          + "<extra></extra>",
        ),
    ]
    fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
    return fig_first_graph


# Update second chart
@app.callback(
    Output("turnout_scatterchart", "figure"),
    Input("referenda-data", "data")
)
def update_bar_chart(referenda_data):
    df_referendum = pd.DataFrame(referenda_data)
    print(df_referendum["turnout_perc"])
    second_graph_data = go.Scatter(
        name="Turnout",
        x=df_referendum.referendum_index.astype(int),
        y=df_referendum["turnout_perc"],
        mode="lines+markers",
        line=dict(color="rgb(0, 0, 100)"),
        marker=dict(color="rgb(0, 0, 100)", size=8),
        hovertemplate="Referendum id: %{x:.0f}<br>"
                      + "Turnout (%): %{y:.4f}<br>"
                      + "<extra></extra>",
    )

    second_graph_layout = go.Layout(
        title="<b>Turnout for selected Referendum IDs</b>",
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Turnout (% of total issued Kusama)", linecolor="#021C1E"),
    )
    fig_second_graph = go.Figure(data=second_graph_data, layout=second_graph_layout)
    return fig_second_graph


# Update piechart
@app.callback(
    output=Output("call_module_piechart", "figure"),
    inputs=Input("referenda-data", "data"))
def update_pie_chart(referenda_data):
    df = pd.DataFrame(referenda_data)
    new_figure = {
        "data": [
            {
                "labels": df["call_module"].value_counts().index.tolist(),
                "values": list(df["call_module"].value_counts()),
                "type": "pie",
                "marker": {"colors": colors, "line": dict(color="white", width=2)},
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


# Running the server
if __name__ == "__main__":
    warnings.filterwarnings(action='ignore')
    app.run_server(port=8088, debug=True)
