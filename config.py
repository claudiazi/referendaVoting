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
