import os

import dash
from flask_caching import Cache

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    # external_stylesheets=external_stylesheets,
)
server = app.server
app.config["suppress_callback_exceptions"] = True


mongodb_url = os.getenv("MONGODB_URL")
db_name = os.getenv("DB_NAME")
table_name = os.getenv("TABLE_NAME")

suffix_row = "_row"
suffix_button_id = "_button"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"
suffix_indicator = "_indicator"

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

theme = {
    "dark": True,
    "detail": "#2d3038",  # Background-card
    "primary": "#007439",  # Green
    "secondary": "#FFD15F",  # Accent
}

# read from subsquid endpoint

cache = Cache(app.server, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "./cache"})