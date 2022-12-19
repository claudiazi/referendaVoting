import os

import dash
from flask_caching import Cache
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.CYBORG]


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=external_stylesheets,
)
server = app.server
app.config["suppress_callback_exceptions"] = True

cache = Cache(app.server, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "./cache"})