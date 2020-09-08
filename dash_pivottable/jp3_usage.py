import dash_pivottable
import dash
import dash_core_components as dcc
from data import data
from dash.dependencies import Input, Output
import dash_html_components as html

import requests
import configparser
import base64
from sys import platform
import json
import os
import pandas as pd
import zlib

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

def auth():
    parser = configparser.ConfigParser()
    if platform == "win32":            
        if parser.read(os.environ['HOMEPATH'] + r'\JP3.ini') == []:
            parser.read(os.environ['USERPROFILE'] + r'\JP3.ini')
        else:
            parser.read(os.environ['HOMEPATH'] + r'\JP3.ini')
    else:
        parser.read(os.environ['HOME'] + r'\JP3.ini')
    
    url = parser["general"]["url"]
    email = parser["general"]["email"]
    pwd = base64.b64decode(parser["general"]["password"]).decode("utf-8")
    params = {'email': email, 'password': pwd}
    r = requests.post(url=url + 'auth/gettoken', data=params)
    token = r.json()['jwt']
    return token, url

creds, url = auth()
params = {'ten_day_bool': False, 'one_day_bool': False, 'user_bool': False}
endpoint = 'noc.samples/sampletabledata/get/'
r = requests.get(url=url + endpoint, params=params, headers={'Authorization': 'Bearer ' + creds})
rsp = json.loads(zlib.decompress(base64.b64decode(r.content)).decode())
df = pd.DataFrame.from_dict(rsp)

df = df[['site_stream', 'start_time', 'analysis_type', 'application',
         'container_type', 'lab', 'method', 'phase', 'process_status',
         'sampler']]
df.start_time = pd.to_datetime(df.start_time)
df['date'] = df.start_time.dt.date
df['year'] = df.start_time.dt.year
df['month'] = df.start_time.dt.month
df['week'] = df.start_time.dt.week
df['day'] = df.start_time.dt.day


data = df.to_dict('records')

app.title = 'My Dash example'
app.layout = html.Div([
    dash_pivottable.PivotTable(
        id='table',
        data=data,
        menuLimit=1000
        # cols=['Day of Week'],
        # colOrder="key_a_to_z",
        # rows=['Party Size'],
        # rowOrder="key_a_to_z",
        # rendererName="Grouped Column Chart",
        # aggregatorName="Average",
        # vals=["Total Bill"],
        # valueFilter={'Day of Week': {'Thursday': False}}
    ),
    dcc.Markdown(
        id='output'
    )
])


# @app.callback(Output('output', 'children'),
#               [Input('table', 'cols'),
#                Input('table', 'rows'),
#                Input('table', 'rowOrder'),
#                Input('table', 'colOrder'),
#                Input('table', 'aggregatorName'),
#                Input('table', 'rendererName')])
# def display_props(cols, rows, row_order, col_order, aggregator, renderer):
#     return """
#         Columns: {}
        
#         rows: {}
        
#         rowOrder: {}
        
#         colOrder: {}
        
#         aggregatorName: {}
        
#         rendererName: {}
#     """.format(str(cols), str(rows), row_order, col_order, aggregator, renderer)


if __name__ == '__main__':
    app.run_server(debug=True)
