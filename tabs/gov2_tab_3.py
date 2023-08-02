import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from config import voting_group_colors, voter_type_colors
from utils.data_preparation import load_specific_account_stats, load_delegation_data
from utils.plotting import blank_figure


gov_version = 2


def build_tab_3():
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
                                    id="account_input",
                                    placeholder="Type in Account Address",
                                    style={
                                        "width": "70%",
                                        "float": "middle",
                                        "color": "black",
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
                            id="gov2_input_warning",
                            children=[
                                dcc.Loading(
                                    id="gov2_account_input_warning",
                                )
                            ],
                        ),
                    ],
                )
            ]
        ),
        html.Div(
            className="twelve columns",
            children=[dcc.Loading(id="gov2_tab3_charts", children=[])],
        ),
        dcc.Store(id="gov2-specific-account-data", data=[], storage_type="memory"),
        dcc.Store(id="gov2-delegation-data", data=[], storage_type="memory"),
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


def build_charts():
    return [
        dcc.Loading(
            id="loading-icon",
            children=[
                html.Div(className="twelve columns", children=[html.Br()]),
                html.Div(
                    className="twelve columns",
                    id="gov2_tab3_card_row_1",
                    children=[],
                ),
                html.Div(className="twelve columns", children=[html.Br()]),
                html.Div(
                    className="twelve columns",
                    id="gov2_tab3_card_row_2",
                    children=[],
                ),
                html.Div(className="twelve columns", children=[html.Br()]),
                html.Div(
                    className="twelve columns",
                    id="gov2_tab3_card_row_3",
                    children=[],
                ),
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
                                        html.Div(
                                            className="twelve columns",
                                            children=[
                                                html.Div(
                                                    className="twelve columns",
                                                    children=[
                                                        daq.ToggleSwitch(
                                                            id="gov2_votes_split_selection",
                                                            label=[
                                                                "Decision",
                                                                "Outcome",
                                                            ],
                                                            value=True,
                                                        )
                                                    ],
                                                ),
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
                                                                id="gov2_voted_amount_barchart",
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
                                                    className="twelve columns",
                                                    children=[html.Br()],
                                                ),
                                                html.Div(
                                                    dcc.Graph(
                                                        className="twelve columns",
                                                        id="gov2_voting_time_distribution",
                                                        figure=blank_figure(),
                                                    )
                                                ),
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
                                    id="iii-chart",
                                    className="twelve columns",
                                    children=[
                                        html.Div(
                                            className="twelve columns",
                                            children=[
                                                dcc.Loading(
                                                    id="loading-icon",
                                                    children=[
                                                        html.Div(
                                                            dcc.Graph(
                                                                id="gov2_delegate_to_chart",
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
                                                        id="gov2_delegated_chart",
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
                                    id="v-chart",
                                    className="twelve columns",
                                    children=[
                                        html.Div(
                                            className="twelve columns",
                                            children=[
                                                dcc.Loading(
                                                    id="loading-icon",
                                                    children=[
                                                        html.Div(
                                                            dcc.Graph(
                                                                id="gov2-voter-type-timeline-chart",
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
                        html.Div(
                            className="six columns graph-block",
                            children=[
                                html.H6(children="Quiz Correctness"),
                                dcc.Loading(
                                    html.Div(
                                        id="gov2-quiz-correctness-table",
                                        children=[],
                                    )
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    ]


layout = build_tab_3()


@app.callback(
    [
        Output("gov2-specific-account-data", "data"),
        Output("gov2-delegation-data", "data"),
        Output("gov2_account_input_warning", "children"),
    ],
    [
        Input("account_input", "value"),
    ],
)
def update_specific_account_data(account_input):
    warning = None
    df_specific_account = pd.DataFrame()
    df_delegation = pd.DataFrame()
    if account_input:
        try:
            df_specific_account = load_specific_account_stats(
                account_input, gov_version
            )
            df_delegation = load_delegation_data(gov_version)
        except:
            warning = dcc.Loading(
                id="loading-icon",
                children=[
                    html.P(
                        className="alert alert-danger",
                        children=[
                            "Possible message: The above wallet is invalid or has not participated in Kusama Governance yet"
                        ],
                    )
                ],
            )
        if df_specific_account.empty:
            warning = dcc.Loading(
                id="loading-icon",
                children=[
                    html.P(
                        className="alert alert-danger",
                        children=[
                            "Possible message: The above wallet is invalid or has not participated in Kusama Governance yet"
                        ],
                    )
                ],
            )
        return (
            df_specific_account.to_dict("records"),
            df_delegation.to_dict("records"),
            [warning],
        )
    return None, None, html.P()


@app.callback(
    output=Output("gov2_tab3_charts", "children"),
    inputs=[
        Input("gov2_account_input_warning", "children"),
    ],
)
def build_gov2_tab3_charts(gov2_input_warning):
    if gov2_input_warning == [None]:
        return build_charts()


@app.callback(
    output=Output("gov2_tab3_card_row_1", "children"),
    inputs=[
        Input("gov2-specific-account-data", "data"),
    ],
)
def update_card1(account_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        return [
            html.Div(
                className="four columns graph-block",
                id="card1",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("First Vote", className="card-title"),
                                    html.P(
                                        f"Timestamp: {df_account['first_voting_timestamp'].unique()[0]}",
                                        className="card-value",
                                    ),
                                    html.P(
                                        f"Referendum ID: {df_account['first_referendum_index'].unique()[0]}",
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
                                    html.H5("# of Ref. Voted", className="card-title"),
                                    html.P(
                                        f"{df_account['referendum_index'].count()}",
                                        className="card-value",
                                    ),
                                    html.P(""),
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
                                    html.H5("Avg. Voted KSM", className="card-title"),
                                    html.P(
                                        f"{df_account['voted_amount_with_conviction'].mean():.2f}",
                                        className="card-value",
                                    ),
                                    html.P(""),
                                ]
                            )
                        ]
                    ),
                ],
            ),
        ]

    return None


@app.callback(
    output=Output("gov2_tab3_card_row_2", "children"),
    inputs=[
        Input("gov2-specific-account-data", "data"),
        Input("gov2-delegation-data", "data"),
    ],
)
def update_card2(account_data, delegation_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_delegation = pd.DataFrame(delegation_data)
        df_delegated = df_delegation.merge(
            df_account, how="inner", left_on="delegated_to", right_on="voter"
        )
        df_delegate_to = df_delegation.merge(
            df_account, how="inner", left_on="wallet", right_on="voter"
        )
        active_delegate_to = df_delegate_to[
            df_delegate_to["delegation_ended_at"].isnull()
        ]["delegated_to_x"].unique()
        if not active_delegate_to:
            active_delegate_to = "None"
        count_active_delegated = len(
            df_delegated[df_delegated["delegation_ended_at"].isnull()][
                "wallet"
            ].unique()
        )
        return [
            html.Div(
                className="four columns graph-block",
                id="card1",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "# of Active delegations",
                                        className="card-title",
                                    ),
                                    html.P(
                                        count_active_delegated,
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
                                    html.H5(
                                        "Active delegate to",
                                        className="card-title",
                                    ),
                                    html.P(
                                        active_delegate_to,
                                        className="card-value",
                                    ),
                                    html.P(""),
                                ]
                            )
                        ]
                    ),
                ],
            ),
        ]

    return None


@app.callback(
    output=Output("gov2_tab3_card_row_3", "children"),
    inputs=[
        Input("gov2-specific-account-data", "data"),
    ],
)
def update_card3(account_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_quizzes = df_account[df_account.correct_answers_count.notnull()]
        return [
            html.Div(
                className="four columns graph-block",
                id="card1",
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "# of Quizzes Taken", className="card-title"
                                    ),
                                    html.P(
                                        f"{df_quizzes['referendum_index'].count()}",
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
                                    html.H5(
                                        "# of Quizzes Fully Correct",
                                        className="card-title",
                                    ),
                                    html.P(
                                        f"{df_quizzes['quiz_fully_correct'].sum()}",
                                        className="card-value",
                                    ),
                                    html.P(""),
                                ]
                            )
                        ]
                    ),
                ],
            ),
        ]

    return None


@app.callback(
    output=Output("gov2_cum_voter_amount_barchart", "figure"),
    inputs=[Input("gov2-specific-referendum-data", "data")],
)
def gov2_cum_voter_amount_barchart(account_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        second_graph_data = [
            go.Scatter(
                name="Aye Votes",
                x=df_account["timestamp"],
                y=df_account["cum_voted_amount_with_conviction_aye"],
                mode="lines",
            ),
            go.Scatter(
                name="Nay Votes",
                x=df_account["timestamp"],
                y=df_account["cum_voted_amount_with_conviction_nay"],
                mode="lines",
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
    output=Output("gov2_voted_amount_barchart", "figure"),
    inputs=[
        Input("gov2-specific-account-data", "data"),
        Input("gov2_votes_split_selection", "value"),
    ],
)
def voter_amount_barchart(account_data, selected_votes_split):
    if account_data:
        df_account = pd.DataFrame(account_data)
        if selected_votes_split == False:
            df_aye = df_account[df_account["decision"] == "aye"]
            df_nay = df_account[df_account["decision"] == "nay"]
            first_graph_data = [
                go.Bar(
                    name="Aye Votes",
                    x=df_aye["referendum_index"],
                    y=df_aye["voted_amount_with_conviction"],
                    marker_color="#ffffff",
                ),
                go.Bar(
                    name="Nay Votes",
                    x=df_nay["referendum_index"],
                    y=df_nay["voted_amount_with_conviction"],
                    marker_color="#e6007a",
                ),
            ]
        else:
            df_aligned = df_account[df_account["voting_result_group"] == "aligned"]
            df_not_aligned = df_account[
                df_account["voting_result_group"] == "not aligned"
            ]
            first_graph_data = [
                go.Bar(
                    name="Aligned with Final Result",
                    x=df_aligned["referendum_index"],
                    y=df_aligned["voted_amount_with_conviction"],
                    marker_color="#ffffff",
                ),
                go.Bar(
                    name="Not Aligned with Final Result",
                    x=df_not_aligned["referendum_index"],
                    y=df_not_aligned["voted_amount_with_conviction"],
                    marker_color="#e6007a",
                ),
            ]

        first_graph_layout = go.Layout(
            title="<b>Voted Amount</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Voted Amount with Conviction", linecolor="#021C1E"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
            template="plotly_dark",
            hovermode="x",
        )
        fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
        fig_first_graph.update_traces(opacity=0.75)
        return fig_first_graph
    return None


@app.callback(
    Output("gov2_voting_time_distribution", "figure"),
    Input("gov2-specific-account-data", "data"),
)
def update_vote_timing_distribution(account_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_voting_group_sum = df_account.groupby("voting_time_group")[
            "referendum_index"
        ].count()
        second_graph_data = [
            go.Pie(
                labels=df_voting_group_sum.index,
                values=df_voting_group_sum.values,
                marker=dict(colors=voting_group_colors),
            )
        ]
        second_graph_layout = go.Layout(
            title="<b>When Wallet Voted</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Count of voting time groups", linecolor="#021C1E"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
            template="plotly_dark",
            hovermode="x",
        )

        fig_second_graph = go.Figure(data=second_graph_data, layout=second_graph_layout)
        return fig_second_graph
    return None


@app.callback(
    output=Output("gov2_delegate_to_chart", "figure"),
    inputs=[
        Input("gov2-specific-account-data", "data"),
        Input("gov2-delegation-data", "data"),
        Input("full-referenda-data", "data"),
    ],
)
def update_gov2_delegate_to_chart(account_data, delegation_data, referenda_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_delegation = pd.DataFrame(delegation_data)
        df_referenda = pd.DataFrame(referenda_data)
        df_delegate_to = df_delegation.merge(
            df_account, how="inner", left_on="wallet", right_on="voter"
        )
        df_delegate_to = df_delegate_to.merge(
            df_referenda, how="inner", on="referendum_index"
        )
        df_delegate_to = df_delegate_to[
            (
                (
                    df_delegate_to["created_at"]
                    >= df_delegate_to["delegation_started_at"]
                )
                & (df_delegate_to["delegation_ended_at"].isnull())
                | (
                    df_delegate_to["created_at"]
                    >= df_delegate_to["delegation_started_at"]
                )
                & (df_delegate_to["ended_at"] <= df_delegate_to["delegation_ended_at"])
            )
        ]

        df_past_delegate_to = df_delegate_to[
            df_delegate_to["delegation_ended_at"].notnull()
        ]
        df_past_delegate_to = (
            df_past_delegate_to.groupby("referendum_index")[
                "voted_amount_with_conviction"
            ]
            .sum()
            .reset_index()
            .sort_values(by="referendum_index")
        )
        df_active_delegate_to = (
            df_delegate_to[(df_delegate_to["delegation_ended_at"].isnull())]
            .groupby("referendum_index")["voted_amount_with_conviction"]
            .sum()
            .reset_index()
            .sort_values(by="referendum_index")
        )
        first_graph_data = [
            go.Bar(
                name="Past Delegate To",
                x=df_past_delegate_to["referendum_index"],
                y=df_past_delegate_to["voted_amount_with_conviction"],
                marker_color="#ffffff",
            ),
            go.Bar(
                name="Active Delegate To",
                x=df_active_delegate_to["referendum_index"],
                y=df_active_delegate_to["voted_amount_with_conviction"],
                marker_color="#e6007a",
            ),
        ]
        first_graph_layout = go.Layout(
            title="<b>Delegation Votes</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Voted Amount with Conviction", linecolor="#021C1E"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
            template="plotly_dark",
            hovermode="x",
        )
        fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
        fig_first_graph.update_traces(opacity=0.75)
        if df_past_delegate_to.empty and df_active_delegate_to.empty:
            fig_first_graph.add_annotation(
                x=1,
                y=1,
                text="No delegation votes",
                showarrow=False,
                yshift=10,
                font=dict(size=16),
            )
        return fig_first_graph
    return None


@app.callback(
    output=Output("gov2_delegated_chart", "figure"),
    inputs=[
        Input("gov2-specific-account-data", "data"),
        Input("gov2-delegation-data", "data"),
        Input("full-referenda-data", "data"),
    ],
)
def update_gov2_delegated_chart(account_data, delegation_data, referenda_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_delegation = pd.DataFrame(delegation_data)
        df_referenda = pd.DataFrame(referenda_data)
        df_delegated = df_delegation.merge(
            df_account, how="inner", left_on="delegated_to", right_on="voter"
        )
        df_delegated = df_delegated.merge(
            df_referenda, how="inner", on="referendum_index"
        )
        df_delegated = df_delegated[
            (
                (df_delegated["created_at"] >= df_delegated["delegation_started_at"])
                & (df_delegated["delegation_ended_at"].isnull())
                | (df_delegated["created_at"] >= df_delegated["delegation_started_at"])
                & (df_delegated["ended_at"] <= df_delegated["delegation_ended_at"])
            )
        ]
        df_past_delegated = df_delegated[df_delegated["delegation_ended_at"].notnull()]
        df_past_delegated = (
            df_past_delegated.groupby("referendum_index")[
                "voted_amount_with_conviction"
            ]
            .sum()
            .reset_index()
            .sort_values(by="referendum_index")
        )
        df_active_delegated = (
            df_delegated[(df_delegated["delegation_ended_at"].isnull())]
            .groupby("referendum_index")["voted_amount_with_conviction"]
            .sum()
            .reset_index()
            .sort_values(by="referendum_index")
        )
        first_graph_data = [
            go.Bar(
                name="Past Delegated",
                x=df_past_delegated["referendum_index"],
                y=df_past_delegated["voted_amount_with_conviction"],
                marker_color="#ffffff",
            ),
            go.Bar(
                name="Active Delegated",
                x=df_active_delegated["referendum_index"],
                y=df_active_delegated["voted_amount_with_conviction"],
                marker_color="#e6007a",
            ),
        ]
        first_graph_layout = go.Layout(
            title="<b>Delegated Votes</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            barmode="stack",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Voted Amount with Conviction", linecolor="#021C1E"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
            template="plotly_dark",
            hovermode="x",
        )
        fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
        fig_first_graph.update_traces(opacity=0.75)
        if df_active_delegated.empty and df_past_delegated.empty:
            fig_first_graph.add_annotation(
                x=1,
                y=1,
                text="No delegated votes",
                showarrow=False,
                yshift=10,
                font=dict(size=16),
            )
        return fig_first_graph
    return None


@app.callback(
    output=Output("gov2-voter-type-timeline-chart", "figure"),
    inputs=[
        Input("gov2-specific-account-data", "data"),
    ],
)
def voter_type_barchart(account_data):
    if account_data:
        df_account = pd.DataFrame(account_data)
        df_normal = df_account[df_account["voter_type"] == "normal"].sort_values(
            "referendum_index"
        )
        df_validator = df_account[df_account["voter_type"] == "validator"].sort_values(
            "referendum_index"
        )
        df_councillor = df_account[
            df_account["voter_type"] == "councillor"
        ].sort_values("referendum_index")
        df_councillor_validator = df_account[
            df_account["voter_type"] == "validator + councillor"
        ].sort_values("referendum_index")
        first_graph_data = [
            go.Scatter(
                name="Normal Votes",
                x=df_normal["referendum_index"],
                y=df_normal["voter_type"],
                marker_color=voter_type_colors[0],
                mode="markers",
            ),
            go.Scatter(
                name="Validator Votes",
                x=df_validator["referendum_index"],
                y=df_validator["voter_type"],
                marker_color=voter_type_colors[1],
                mode="markers",
            ),
            go.Scatter(
                name="Councillor Votes",
                x=df_councillor["referendum_index"],
                y=df_councillor["voter_type"],
                marker_color=voter_type_colors[2],
                mode="markers",
            ),
            go.Scatter(
                name="Councillor + Validator Votes",
                x=df_councillor_validator["referendum_index"],
                y=df_councillor_validator["voter_type"],
                marker_color=voter_type_colors[3],
                mode="markers",
            ),
        ]
        first_graph_layout = go.Layout(
            title="<b>Voter Type Timeline</b>",
            paper_bgcolor="#161a28",
            plot_bgcolor="#161a28",
            xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
            yaxis=dict(title="Voter Type", linecolor="#021C1E"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
            template="plotly_dark",
            hovermode="x",
        )
        fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
        fig_first_graph.update_traces(opacity=0.75)
        return fig_first_graph
    return None


@app.callback(
    Output("gov2-quiz-correctness-table", "children"),
    inputs=[Input("gov2-specific-account-data", "data")],
)
def create_quiz_correctness_table(account_data):
    df = pd.DataFrame(account_data)
    df = df[df["correct_answers_count"].notnull()]
    if not df.empty:
        df["quiz_correctness"] = df.apply(
            lambda row: f"{row['correct_answers_count']:.0f} / {row['questions_count']:.0f}",
            axis=1,
        )
        df = df[["referendum_index", "quiz_correctness"]]
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
            page_size=10,
            style_table={"height": "350px", "overflowY": "auto"},
        )
    else:
        my_table = html.P("No quizzes attended.")
    return my_table
