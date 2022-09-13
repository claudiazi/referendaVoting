import warnings

import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from tabs import tab_1, tab_2, tab_3
from utils.data_preparation import (
    preprocessing_referendum,
    preprocessing_votes,
)


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.H1("Kusama Governance Dashboard - Referendum Analysis"),
        ],
    )

def build_tabs():
    return dcc.Tabs(
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
                        id="Referendum-tab",
                        label="Single Referendum View",
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
                    dcc.Tab(
                        id="Single-account-tab",
                        label="Single Account View",
                        value="tab3",
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
                ])


server = app.server
app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=0,
            disabled=True,
        ),
        dcc.Interval(
            id="interval-component-live",
            interval=300,  # in milliseconds
            n_intervals=0,
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                html.Div(id="app-content"),
            ],
        ),
        # Main app
        dcc.Store(id="raw-data", data=[], storage_type="memory"),
        dcc.Store(id="votes-data", data=[], storage_type="memory"),
        dcc.Store(
            id="referenda-data",
            data=[],
            storage_type="memory",
        ),
        dcc.Store(id="ongoing-referenda-data", data=[], storage_type="memory"),
        dcc.Store(id="n-interval-stage", data=0),
    ],
)


def load_refined_referenda_data():
    # df_raw = load_data(mongodb_url=mongodb_url, db_name=db_name, table_name=table_name)
    df_raw = pd.read_csv("../referendum_data.csv")
    df_referendum = preprocessing_referendum(df_raw)
    print("referendum data loaded!")
    return df_referendum.to_dict("record")


def load_refined_votes_data():
    # df_raw = load_data(mongodb_url=mongodb_url, db_name=db_name, table_name=table_name)
    df_raw = pd.read_csv("../votes_data.csv")
    df_votes = preprocessing_votes(df_raw)
    print("votes data loaded!")
    return df_votes.to_dict("record")


@app.callback(
    [
        Output("referenda-data", "data"),
        Output("votes-data", "data"),
    ],
    [Input("interval-component", "n_intervals")],
)
def update_historical_data(n_intervals):
    if n_intervals >= 0:
        refined_referenda_data = load_refined_referenda_data()
        refined_votes_data = load_refined_votes_data()

        return (
            refined_referenda_data,
            refined_votes_data,
        )


@app.callback(
    Output("app-content", "children"),
    Input("app-tabs", "value")
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return tab_1.layout
    if tab_switch == "tab2":
        return tab_2.layout
    return tab_3.layout


# # Running the server
if __name__ == "__main__":
    warnings.filterwarnings(action="ignore")
    app.run_server(port=8088, debug=True)