from dash import dcc
from dash import html

layout = html.Div(
            id="status-container",
            children=[
                html.H3("Tab content 1"),
                dcc.Graph(
                    figure={"data": [{"x": [1, 2, 3], "y": [3, 1, 2], "type": "bar"}]}
                ),
            ],
        )