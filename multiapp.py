"""Frameworks for running multiple Streamlit applications as a single app.
"""
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu


class MultiApp:
    """Framework for combining multiple streamlit applications."""

    def __init__(self, df: pd.DataFrame):
        self.apps = []
        self.df = df

    def add_app(self, title, icon, func):
        """Adds a new application.
        :param title: title of the app, appears in the dropdown in the sidebar.
        :param icon:the icon of the app, appears in the dropdown in the sidebar.
        :param func:the python function to render this app.
        """
        self.apps.append(
            {
                "title": title,
                "icon": icon,
                "function": func,
            }
        )

    def run(self):
        st.set_page_config(layout="wide")
        with st.sidebar:
            choose = option_menu(
                "Dashboards",
                options=[app["title"] for app in self.apps],
                icons=[app["icon"] for app in self.apps],
                menu_icon="app-indicator",
                default_index=0,
                styles={
                    "container": {
                        "padding": "5!important",
                        "background-color": "#fafafa",
                    },
                    "icon": {"color": "#006464", "font-size": "25px"},
                    "nav-link": {
                        "font-size": "16px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#eee",
                    },
                    "nav-link-selected": {"background-color": "#00c8c8"},  ##02ab21
                },
            )
        for app in self.apps:
            if choose == app["title"]:
                app["function"](self.df)
