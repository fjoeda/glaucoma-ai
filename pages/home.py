import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import base64
import io
from PIL import Image
import re

from app import app

from style import CONTENT_STYLE, UPLOAD_CONTENT_STYLE
from helpers.predict import ImagePredictor

pred = ImagePredictor()

home_layout = [
    html.Div([
        dbc.Row([
            html.Div([
                    dcc.Upload([
                        'Drag and Drop or ',
                        html.A('Select a File')
                    ], style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center'
                    }, id="upload-image"),
                    html.Br(),
                    dbc.Row([
                        html.Div(id='output-image-upload')
                    ],justify="center", align="center")
            ], style=CONTENT_STYLE),
            html.Div([
                html.H1("Result", ),
                html.Hr(),
                html.Div([
                    dbc.Row([
                        dbc.Col(html.H5("Glaucoma Positive : "),width = 2),
                        dbc.Col(dbc.Progress(id="positive", color = 'danger', value = 80))
                    ],justify="center", align="center"),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.H5("Glaucoma Negative : "),width = 2),
                        dbc.Col(dbc.Progress(id="negative", color = 'success', value = 80))
                    ],justify="center", align="center"),
                ])
            ],  style=CONTENT_STYLE),
        ])
    ])
]


def decode_img(msg):
    msg = re.sub('^data:image/.+;base64,', '',msg)
    msg = base64.b64decode(msg)
    buf = io.BytesIO(msg)
    img = Image.open(buf)
    return img


@app.callback(
    [Output("output-image-upload","children"),Output("positive","value"),Output("negative","value")],
    [Input('upload-image','contents')]
)
def update_value(content):
    if content is not None:
        image_content = html.Div([
            html.Img(src=content, style={'height':'300px'})
        ])
        img = decode_img(content)
        negative, positive = pred.predict(img)
        
        positive_val = round(positive*100)
        negative_val = round(negative*100)
        #positive_val = 10
        #negative_val = 20
        return image_content, positive_val, negative_val

