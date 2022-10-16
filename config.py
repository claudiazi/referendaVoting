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

voting_group_colors = ["#ffffff", "#ffb3e0", "#ff33ad", "#e6007a"]

color_scale = [
    "#ffffff",
    "#ffe6f3",
    "#ffb3e0",
    "#ff84c5",
    "#ff80cc",
    "#ff66c2",
    "#ff4db8",
    "#ff33ad",
    "#ff1aa3",
    "#ff2297",
    "#e6007a",
    "#cc007a",
    "#b3006b",
    "#ff0e8e",
    "#fa0084",
    "#ff2297",
    "#ff49aa",
    "#ab005b",
    "#840046",
    "#70003c",
]

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
