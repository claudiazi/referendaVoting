import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.patches as mpatches

import numpy as np
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px


from data_preparation import load_data, preprocessing

st.title("Referendum Voting")

st.markdown(
    """
This app performs simple analysis about the past referendum votes.
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [kusama].
"""
)

st.sidebar.header("User Input Features")
mongodb_url = os.getenv("MONGODB_URL")
db_name = os.getenv("DB_NAME")
table_name = os.getenv("TABLE_NAME")
votes_df = load_data(mongodb_url=mongodb_url, db_name=db_name, table_name=table_name)
votes_df = preprocessing(votes_df)

# Sidebar - Referendum selection
referendum_ids = sorted(votes_df.id.unique())
max_id = int(max(referendum_ids))
min_id = int(min(referendum_ids))
selected_ids = st.sidebar.slider(
    "Select a range of ids",
    min_value=min_id,
    max_value=max_id,
    value=[min_id, max_id],
    step=1,
)
votes_df = votes_df[
    (votes_df["id"] >= selected_ids[0]) & (votes_df["id"] <= selected_ids[1])
]

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

layout = go.Layout(
    title="<b>Vote counts for selected Referendum IDs</b>",
    paper_bgcolor="rgb(248, 248, 255)",
    plot_bgcolor="rgb(248, 248, 255)",
    barmode="stack",
    xaxis=dict(title="Referendum ID", linecolor="#BCCCDC"),
    yaxis=dict(title="Vote counts", linecolor="#021C1E"),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
)

total_count = np.transpose([df_delegated_count_sum["id"], df_delegated_count_sum["vote_counts"] + df_non_delegated_count_sum["vote_counts"]])

data = [
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

fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig)


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
    df_votes_balance_perc["balance_sum"] / df_votes_balance_perc["total_issuance"] * 100
)

with sns.axes_style("white"):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.pointplot(
        x=df_votes_balance_perc.id.astype(int),
        y="perc",
        marker="o",
        data=df_votes_balance_perc,
        color="darkkhaki",
    )
    ax.set(
        xlabel="Referendum ID",
        ylabel="Turnout (% of total issued Kusama)",
        title="Turnout for selected Referendum IDs",
    )
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
st.pyplot(fig)

# Third Chart
df_first_votes = (
    votes_df.groupby("accountId")["id"].min().reset_index(name="first_voted_id")
)
votes_df = votes_df.merge(df_first_votes, on="accountId")
votes_df.loc[votes_df["id"] == votes_df["first_voted_id"], "is_new"] = 1
votes_df.loc[votes_df["id"] != votes_df["first_voted_id"], "is_new"] = 0
df_counts_new = votes_df.groupby("id")["is_new"].sum().reset_index(name="counts_new")
df_counts_new = pd.merge(df_counts_new, df_count_sum, on="id")
df_counts_new["new_perc"] = (
    df_counts_new["counts_new"] / df_counts_new["vote_counts"] * 100
)
with sns.axes_style("white"):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        x=df_counts_new.id,
        y="counts_new",
        data=df_counts_new,
        color="palegoldenrod",
    )
    ax2 = ax.twinx()
    sns.pointplot(
        x=df_counts_new.id,
        y="new_perc",
        marker="o",
        data=df_counts_new,
        color="darkkhaki",
    )
    ax.set(
        xlabel="Referendum ID",
        ylabel="New accounts counts",
        title="New accounts counts for selected Referendum IDs",
    )
    ax2.set(ylabel="New accounts counts (% of total votes counts)")
    barplot = mpatches.Patch(color="palegoldenrod", label="New accounts counts")
    lineplot = mpatches.Patch(color="darkkhaki", label="% of total votes counts")
    plt.legend(handles=[barplot, lineplot])
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    st.pyplot(fig)

df_higest_balance_user = votes_df.groupby("accountId")["balance"].sum().reset_index()
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
