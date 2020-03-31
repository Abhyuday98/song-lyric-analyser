import pandas as pd
import glob
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from song_finder import find_song

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

# Load az-lyrics dataset
all_files = glob.glob("data/*.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, error_bad_lines=False, warn_bad_lines=False)
    li.append(df)
df = pd.concat(li, axis=0, ignore_index=True)
df = df.dropna()

# To store if phrase submit button is clicked
clicks = 1

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

HIDDEN_STYLE = {
    'display': 'none',
}

sidebar = html.Div(
    [
        html.H2("IS450 - G1", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Topic Extraction", href="/page-1", id="page-1-link"),
                dbc.NavLink("Song Finder", href="/page-2", id="page-2-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content,

    # Hidden
    dbc.Input(id="phrase-input", style=HIDDEN_STYLE),
    html.Div(id='song-finder-output', style=HIDDEN_STYLE),
    dbc.Button('Submit', id='phrase-submit', style=HIDDEN_STYLE)
])

page_1 = html.Div([
])

page_2 = html.Div([
    html.P(
        'Heard some part of a song but can\'t recall which song it belonged? ' +
        'Use the Song Finder to search for your song and restore your sanity!'
    ),
    dbc.Form([
        dbc.Input(id="phrase-input", placeholder="Enter Phrase", type="text", style={'width': '400px'}),
        dbc.Button('Submit', id='phrase-submit')
    ], inline=True),
    html.Br(),
    dcc.Loading(
        id='loading-phrase',
        children=[html.Div(id="song-finder-output")],
        type='default',
        color='black'
    ),
])


# Call back to change pages
@app.callback([Output(f"page-{i}-link", "active") for i in range(1, 3)], [Input("url", "pathname")])
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 3)]


# Call back to show page content from sidebar
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        global clicks
        clicks = 1
        return page_1
    elif pathname == "/page-2":
        return page_2
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


# Call back to show page 2 content
@app.callback(Output('song-finder-output', 'children'), [
    Input('phrase-input', 'value'),
    Input('phrase-submit', 'n_clicks')
])
def render_song_finder_output(input_phrase, n):
    if not input_phrase:
        return html.Div()

    global df
    global clicks
    if n == clicks:
        clicks += 1
        song, phrase = find_song(df, input_phrase)
        return html.Div([
            html.H6('Song'),
            html.P(song),
            html.H6('Exact Phrase'),
            html.P(phrase),
            html.H6('Youtube'),
            html.P(phrase)
        ])

    raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
