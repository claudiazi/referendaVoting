voting_group_dict = {
    "count_0_4_1_4_vote_duration": "0/4 - 1/4 vote duration",
    "count_1_4_2_4_vote_duration": "1/4 - 2/4 vote duration",
    "count_2_4_3_4_vote_duration": "2/4 - 3/4 vote duration",
    "count_3_4_4_4_vote_duration": "3/4 - 4/4 vote duration",
}

voting_group_perc_dict = {
    "count_0_4_1_4_vote_duration_perc": "0/4 - 1/4 vote duration",
    "count_1_4_2_4_vote_duration_perc": "1/4 - 2/4 vote duration",
    "count_2_4_3_4_vote_duration_perc": "2/4 - 3/4 vote duration",
    "count_3_4_4_4_vote_duration_perc": "3/4 - 4/4 vote duration",
}

voting_group_colors = ["gold", "mediumturquoise", "darkorange", "lightgreen"]

referendum_columns = [
    "referendum_index",
    "pre_image_author_address",
    "pre_image_call_module",
    "pre_image_call_name",
    "status",
    "delay",
    "duration",
    "aye_amount",
    "aye_without_conviction",
    "nay_amount",
    "nay_without_conviction",
    "total_issuance",
    "turnout",
    "executed_success",
]

votes_columns = [
    "referendum_index",
    "account_address",
    "voting_time",
    "amount",
    "conviction",
    "passed"
    # "isAye",
    # "isNay",
    # "isDelegating",
]

ongoing_refenrenda_columns = [
    "referendum_index",
    "threshold",
    "ayes_perc",
    "end",
    "turnout",
]

referendum_columns_convert_to_int = [
    "turnout",
    "total_issuance",
    "aye_without_conviction",
    "nay_without_conviction",
    "aye_amount",
    "nay_amount",
]

votes_columns_convert_to_float = [
    "conviction",
    "amount",
]
