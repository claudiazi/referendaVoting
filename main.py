import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

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

votes_df = load_data()
votes_df = preprocessing(votes_df)

# Sidebar - Referendum selection
sorted_referendum_id = sorted(votes_df.id.unique())
selected_id = st.sidebar.multiselect(
    "Referendum ID", sorted_referendum_id, sorted_referendum_id
)

df_balance_sum = (
    votes_df.groupby("id")["balance"]
    .sum()
    .reset_index(name="balance_sum")
    .sort_values(by="id")
)
df_count_sum = (
    votes_df.groupby("id")["accountId"]
    .count()
    .reset_index(name="vote_counts")
    .sort_values(by="id")
)
df_sum = pd.merge(df_balance_sum, df_count_sum)
with sns.axes_style("white"):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax1 = sns.barplot(x="id", y="balance_sum", data=df_sum)
    ax2 = plt.twinx()
    sns.barplot(x="id", y="vote_counts", data=df_sum, ax=ax2)
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
