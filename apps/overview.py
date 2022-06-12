import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.data_preparation import load_data, preprocessing


def app(df: pd.DataFrame):
    st.title("Referendum Voting")

    st.markdown(
        """
    This app performs simple analysis about the past referendum votes.
    * **Data source:** [kusama].
    """
    )

    st.sidebar.header("User Input Features")

    # Sidebar - Referendum selection
    referendum_ids = sorted(df.id.unique())
    max_id = int(max(referendum_ids))
    min_id = int(min(referendum_ids))
    selected_ids = st.sidebar.slider(
        "Select a range of ids",
        min_value=min_id,
        max_value=max_id,
        value=[min_id, max_id],
        step=1,
    )

    votes_df = df[(df["id"] >= selected_ids[0]) & (df["id"] <= selected_ids[1])]

    df_count_sum = (
        votes_df.groupby(["time", "id"])["accountId"]
        .count()
        .reset_index(name="vote_counts")
        .sort_values(by="id")
    )

    # First Chart
    # top bar -> sum all votes (delegated/ non-delegated)

    # delegated=False votes
    df_non_delegated = votes_df[votes_df["isDelegating"] == False]
    df_non_delegated_count_sum = (
        df_non_delegated.groupby(["time", "id"])["accountId"]
        .count()
        .reset_index(name="vote_counts")
        .sort_values(by="id")
    )

    # delegated=True votes
    df_delegated = votes_df[votes_df["isDelegating"] == True]
    df_delegated_count_sum = (
        df_delegated.groupby(["time", "id"])["accountId"]
        .count()
        .reset_index(name="vote_counts")
        .sort_values(by="id")
    )

    # COLORS_MAPPER = {
    #     "Delegated Votes": "rgb(0, 0, 100)",
    #     "Non-delegated Votes": "rgb(0, 200, 200)",
    # }

    first_graph_layout = go.Layout(
        title="<b>Vote counts for selected Referendum IDs</b>",
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        barmode="stack",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Vote counts", linecolor="#021C1E"),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )

    total_count = np.transpose(
        [
            df_delegated_count_sum["id"],
            df_delegated_count_sum["vote_counts"]
            + df_non_delegated_count_sum["vote_counts"],
        ]
    )

    first_graph_data = [
        go.Bar(
            name="Delegated Votes",
            x=df_delegated_count_sum["id"],
            y=df_delegated_count_sum["vote_counts"],
            marker_color="rgb(0, 0, 100)",
            customdata=total_count,
            hovertemplate="<b>Delegated Votes</b><br><br>"
            + "Referendum id: %{x:.0f}<br>"
            + "Vote counts: %{y:.0f}<br>"
            + "Total counts: %{customdata[1]:.0f}<br>"
            + "<extra></extra>",
        ),
        go.Bar(
            name="Non-delegated Votes",
            x=df_non_delegated_count_sum["id"],
            y=df_non_delegated_count_sum["vote_counts"],
            customdata=total_count,
            marker_color="rgb(0, 200, 200)",
            hovertemplate="<b>Non-delegated Votes</b><br><br>"
            + "Referendum id: %{x:.0f}<br>"
            + "Vote counts: %{y:.0f}<br>"
            + "Total counts: %{customdata[1]:.0f}<br>"
            + "<extra></extra>",
        ),
    ]
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        fig_first_graph = go.Figure(data=first_graph_data, layout=first_graph_layout)
        st.plotly_chart(fig_first_graph)

    # Second chart
    df_balance_sum = (
        votes_df.groupby(["time", "id"])["balance"]
        .sum()
        .reset_index(name="balance_sum")
        .sort_values(by="id")
    )

    df_total_issuance_sum = (
        votes_df.groupby(["time", "id"])["totalIssuance"]
        .mean()
        .reset_index(name="total_issuance")
        .sort_values(by="id")
    )

    df_votes_balance_perc = df_balance_sum.merge(
        df_total_issuance_sum, how="inner", on=["id", "time"]
    )
    df_votes_balance_perc["perc"] = (
        df_votes_balance_perc["balance_sum"]
        / df_votes_balance_perc["total_issuance"]
        * 100
    )

    second_graph_data = go.Scatter(
        name="Turnout",
        x=df_votes_balance_perc.id.astype(int),
        y=df_votes_balance_perc["perc"],
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

    # Third Chart
    df_first_votes = (
        votes_df.groupby("accountId")["id"].min().reset_index(name="first_voted_id")
    )
    votes_df = votes_df.merge(df_first_votes, on="accountId")
    votes_df.loc[votes_df["id"] == votes_df["first_voted_id"], "is_new"] = 1
    votes_df.loc[votes_df["id"] != votes_df["first_voted_id"], "is_new"] = 0
    df_counts_new = (
        votes_df.groupby("id")["is_new"].sum().reset_index(name="counts_new")
    )
    df_counts_new = pd.merge(df_counts_new, df_count_sum, on="id")
    df_counts_new["new_perc"] = (
        df_counts_new["counts_new"] / df_counts_new["vote_counts"] * 100
    )

    third_graph_data = [
        go.Bar(
            name="New accounts counts",
            x=df_counts_new["id"],
            y=df_counts_new["counts_new"],
            marker_color="rgb(0, 200, 200)",
            hovertemplate="Referendum id: %{x:.0f}<br>"
            + "New accounts counts: %{y:.0f}<br>"
            + "<extra></extra>",
        ),
        go.Scatter(
            name="% of total votes counts",
            x=df_counts_new["id"],
            y=df_counts_new["new_perc"],
            mode="lines+markers",
            yaxis="y2",
            line=dict(color="rgb(0, 0, 100)"),
            marker=dict(color="rgb(0, 0, 100)", size=8),
            hovertemplate="Referendum id: %{x:.0f}<br>"
            + "% of total votes counts: %{y:.4f}<br>"
            + "<extra></extra>",
        ),
    ]

    third_graph_layout = go.Layout(
        title="<b>Turnout for selected Referendum IDs</b>",
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
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        fig_third_graph = go.Figure(data=third_graph_data, layout=third_graph_layout)
        st.plotly_chart(fig_third_graph)

    ## Forth part
    df_conviction_mean = votes_df[["id", "conviction"]].groupby("id").mean()
    df_conviction_median = votes_df[["id", "conviction"]].groupby("id").median()
    # df_conviction = pd.merge(df_conviction_mean, df_conviction_median, on='id')

    df_voted_ksm_mean = votes_df[["id", "voted_ksm"]].groupby("id").mean()
    df_voted_ksm_median = votes_df[["id", "voted_ksm"]].groupby("id").median()

    forth_graph_data_1 = [
        go.Scatter(
            name="mean",
            x=df_conviction_mean.index,
            y=df_conviction_mean["conviction"],
            mode="lines+markers",
            line=dict(color="rgb(0, 0, 100)"),
            marker=dict(color="rgb(0, 0, 100)", size=8),
            hovertemplate="Referendum id: %{x:.0f}<br>"
            + "conviction mean: %{y:.4f}<br>"
            + "<extra></extra>",
        ),
        go.Scatter(
            name="median",
            x=df_conviction_median.index,
            y=df_conviction_median["conviction"],
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="rgb(0, 200, 200)"),
            marker=dict(color="rgb(0, 200, 200)", size=8),
            hovertemplate="Referendum id: %{x:.0f}<br>"
            + "conviction median: %{y:.4f}<br>"
            + "<extra></extra>",
        ),
    ]

    forth_graph_data_2 = [
        go.Scatter(
            name="mean",
            x=df_voted_ksm_mean.index,
            y=df_voted_ksm_mean["voted_ksm"],
            mode="lines+markers",
            line=dict(color="rgb(0, 0, 100)"),
            marker=dict(color="rgb(0, 0, 100)", size=6),
            hovertemplate="Referendum id: %{x:.0f}<br>"
            + "voted ksm mean: %{y:.4f}<br>"
            + "<extra></extra>",
        ),
        go.Scatter(
            name="median",
            x=df_voted_ksm_median.index,
            y=df_voted_ksm_median["voted_ksm"],
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="rgb(0, 200, 200)", dash="dash"),
            marker=dict(color="rgb(0, 200, 200)", size=6),
            hovertemplate="Referendum id: %{x:.0f}<br>"
            + "voted ksm median: %{y:.4f}<br>"
            + "<extra></extra>",
        ),
    ]

    forth_graph_layout_1 = go.Layout(
        title="<b>Conviction Mean and Median for selected Referendum IDs</b>",
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Conviction Mean", linecolor="#021C1E"),
        yaxis2=dict(
            title="Conviction Median",
            linecolor="#021C1E",
            anchor="x",
            overlaying="y",
            side="right",
        ),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )

    forth_graph_layout_2 = go.Layout(
        title="<b>Voted KSM Mean and Median for selected Referendum IDs</b>",
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Voted KSM", linecolor="#021C1E"),
        yaxis2=dict(
            title="Voted KSM Median",
            linecolor="#021C1E",
            anchor="x",
            overlaying="y",
            side="right",
        ),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )

    fig_forth_graph_1 = go.Figure(data=forth_graph_data_1, layout=forth_graph_layout_1)
    fig_forth_graph_2 = go.Figure(data=forth_graph_data_2, layout=forth_graph_layout_2)

    col1, col2 = st.columns([1, 1])
    for (col, fig) in zip([col1, col2], [fig_forth_graph_1, fig_forth_graph_2]):
        with col:
            st.plotly_chart(fig, use_container_width=True)

    # Fifth chart
    df_locked_amount_mean = votes_df[["id", "locked_amount"]].groupby("id").mean()
    df_locked_amount_median = votes_df[["id", "locked_amount"]].groupby("id").median()
    df_locked_amount_75_quantile = (
        votes_df[["id", "locked_amount"]].groupby("id").quantile(0.75)
    )

    fifth_graph_data = [
        go.Scatter(
            name="mean",
            x=df_locked_amount_mean.index,
            y=df_locked_amount_mean["locked_amount"],
            mode="lines+markers",
            line=dict(color="rgb(0, 0, 100)", dash="dot"),
            marker=dict(color="rgb(0, 0, 100)", size=6),
            hovertemplate="Referendum id: %{x:.0f}<br>"
            + "locked amount mean: %{y:.4f}<br>"
            + "<extra></extra>",
        ),
        go.Scatter(
            name="median",
            x=df_locked_amount_median.index,
            y=df_locked_amount_median["locked_amount"],
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="rgb(0, 200, 200)", dash="dash"),
            marker=dict(color="rgb(0, 200, 200)", size=6),
            hovertemplate="Referendum id: %{x:.0f}<br>"
            + "locked amount median: %{y:.4f}<br>"
            + "<extra></extra>",
        ),
        go.Scatter(
            name="75th quantile",
            x=df_locked_amount_75_quantile.index,
            y=df_locked_amount_75_quantile["locked_amount"],
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="rgb(255, 53, 184)"),
            marker=dict(color="rgb(255, 53, 184)", size=6, symbol="square"),
            hovertemplate="Referendum id: %{x:.0f}<br>"
            + "locked amount 75th quantile: %{y:.4f}<br>"
            + "<extra></extra>",
        ),
    ]

    fifth_graph_layout = go.Layout(
        title="<b>Locked KSM Mean and Median for selected Referendum IDs</b>",
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
        yaxis=dict(title="Locked KSM - Mean", linecolor="#021C1E"),
        yaxis2=dict(
            title="Locked KSM - Median & Quantile",
            linecolor="#021C1E",
            anchor="x",
            overlaying="y",
            side="right",
        ),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        fig_fifth_graph = go.Figure(data=fifth_graph_data, layout=fifth_graph_layout)
        st.plotly_chart(fig_fifth_graph)

    ## second table
    df_higest_balance_user = (
        votes_df.groupby("accountId")["balance"].sum().reset_index()
    )
    df_higest_balance_user = df_higest_balance_user.sort_values(
        by="balance", ascending=False
    ).reset_index(drop=True)
    st.header("Display Accounts with highest balance")
    st.dataframe(df_higest_balance_user)
    # st.table(df_most_voted_user.assign(hack='').set_index('hack'))

    referenda_counts = votes_df["id"].nunique()
    df_most_voted_user = (
        votes_df.groupby("accountId")["id"].count().reset_index(name="count")
    )
    df_most_voted_user = df_most_voted_user.sort_values(
        by="count", ascending=False
    ).reset_index(drop=True)
    df_most_voted_user["prct"] = df_most_voted_user["count"] / referenda_counts
    st.header("Display Accounts with most votes")
    st.dataframe(df_most_voted_user)
