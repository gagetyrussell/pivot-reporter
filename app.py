# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 11:01:39 2020

@author: GRussell
"""

import dash_pivottable
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html

import pandas as pd
import base64
import io

import webbrowser

def upload_2_df(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename.lower():
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename.lower():
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'xlsx' in filename.lower():
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    
    return df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = 'GTR Spreadsheet Viewer'
app.layout = html.Div([
    html.Div([
        html.Img(src=app.get_asset_url("gtr_data_solutions_logo.png")),
        dcc.Upload(
            className="four columns",
            id='upload-spreadsheet',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Spreadsheet'),
                ' Your data is not being uploaded anywhere. Everything will remain local to your machine.'
            ]),
            style={
                'width': '98%',
                'height': '100px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
            },
            # Allow multiple files to be uploaded
            multiple=False
        ),
    ]),
    html.Div(id='pivot-div')

])

@app.callback(Output('pivot-div', 'children'),
              [Input('upload-spreadsheet', 'contents')],
              [State('upload-spreadsheet', 'filename')])
def show_edd(contents, filename):
    if contents is not None:
        df = upload_2_df(contents, filename)
        data = df.to_dict('records')
        pivot = dash_pivottable.PivotTable(
            id='table',
            data=data,
            menuLimit=5000
        )
        return pivot

if __name__ == '__main__':
    webbrowser.open("http://localhost:8050")
    app.run_server(debug=False, port=8050)
