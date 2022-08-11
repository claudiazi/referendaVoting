referendum_columns = [
    "referendum_index",
    "total_issuance",
    "created_block",
    "updated_block",
    "vote_threshold",
    "pre_image",
    "value",
    "status",
    "delay",
    "end",
    "timeline",
    "aye_amount",
    "nay_amount",
    "turnout",
    "executed_success",
    "aye_without_conviction",
    "nay_without_conviction",
]

votes_columns = [
    "referendum_index",
    "account.address",
    "voting_time",
    "amount",
    "conviction",
    # "isAye",
    # "isNay",
    # "isDelegating",
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
