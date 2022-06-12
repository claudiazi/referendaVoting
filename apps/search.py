import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def app(df: pd.DataFrame):
    st.title("Anaysis of a specific account")

    input_user = st.text_input("Enter the address you want to search:")
    has_user_input = False
    if input_user not in df["accountId"].unique():
        st.warning(
            "Sorry we can't find this account, please check the acocunt address again. :)"
        )
        has_user_input = False
    else:
        selected_user_df = df[df["accountId"] == input_user][
            [
                "id",
                "passed",
                "time",
                "conviction",
                "isAye",
                "isDelegating",
                "isEmpty",
                "voted_ksm",
                "locked_amount",
            ]
        ].reset_index(drop=True)
        has_user_input = True

    ## Table
    if has_user_input:
        first_table_data = go.Table(
            columnwidth=[50, 50, 50, 50, 50, 50, 50, 50, 50],
            header=dict(values=list(selected_user_df.columns), align="left"),
            cells=dict(
                values=[
                    selected_user_df[col].values for col in selected_user_df.columns
                ],
                align="left",
            ),
        )
        first_table_layout = go.Layout(
            title="<b>Basic referendum information</b>", width=1200
        )

        fig_first_table = go.Figure(data=first_table_data, layout=first_table_layout)
        st.plotly_chart(fig_first_table)
