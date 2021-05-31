import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output

from app import app
from pages import home


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("AI Assistant for Glaucoma Detection Demo", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="#",
        ),
    ],
    color="dark",
    dark=True,
)

content = html.Div(id='page-content',children=[])

app.layout = html.Div([
    dcc.Location(id='url'),
    navbar,
    content
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/":
        return home.home_layout

if __name__ == '__main__':
    app.run_server(debug=False)