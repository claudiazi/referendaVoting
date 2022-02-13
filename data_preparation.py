import pandas as pd
import json


def load_data():
    with open("localStorage.json") as data_file:
        data = json.load(data_file)
    df = pd.json_normalize(data["referenda"], record_path="votes", meta="id")
    return df


def preprocessing(df: pd.DataFrame):
    df["balance"] = pd.to_numeric(df["balance"]).apply(lambda x: x / 1000000000)
    return df
