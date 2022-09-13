from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
from app import app

def build_tab_2():
    return [
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(className="twelve columns", children=[html.Br()]),
        html.Div(
            className="section-banner",
            children=[
                html.Div(
                    className="twelve columns",
                    children=[
                        html.P(
                            "Type in the Referendum index: ",
                            style={"display": "inline-block", "margin-right": "8px"},
                        ),
                        dcc.Input(id="referendum_input", placeholder="number"),
                        html.Div(id="referendum_input_warning", children=[]),
                    ],
                ),
                html.Button(
                    "Confirm",
                    id="referendum-trigger-btn",
                    n_clicks=0,
                    style={"display": "inline-block", "float": "middle"},
                ),
            ],
        ),
        dcc.Store(id="specific-referendum-data", data=[], storage_type="memory"),
        dcc.Store(id="specific-referendum-votes-data", data=[], storage_type="memory"),
    ]

layout = build_tab_2()

# Callback to update the referendum df
@app.callback(
    [
        Output("specific-referendum-data", "data"),
        Output("specific-referendum-votes-data", "data"),
        Output("referendum_input_warning", "children"),
    ],
    [
        Input("referendum-trigger-btn", "n_clicks"),
        Input("referendum_input", "value"),
        Input("referenda-data", "data"),
        Input("votes-data", "data"),
    ],
)
def update_specific_referendum_data(
    n_clicks, referendum_input, referenda_data, votes_data
):
    warning = None
    df_specific_referendum = pd.DataFrame()
    if referendum_input:
        df_referenda = pd.DataFrame(referenda_data)
        df_votes = pd.DataFrame(votes_data)
        try:
            df_specific_referendum = df_referenda[
                df_referenda.referendum_index == int(referendum_input)
            ]
            df_specific_referendum_votes = df_votes[
                df_votes.referendum_index == int(referendum_input)
            ]
        except:
            warning = html.P(
                className="alert alert-danger", children=["Invalid input"]
            )
        if df_specific_referendum.empty:
            warning = html.P(
                className="alert alert-danger", children=["Invalid input"]
            )
        return (
            df_specific_referendum.to_dict("record"),
            df_specific_referendum_votes.to_dict("record"),
            [warning],
        )
    return None, None, html.P()

