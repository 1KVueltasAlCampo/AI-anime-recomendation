import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import sys
import os
import pandas as pd 


app = dash.Dash('app_name')

df = pd.read_csv('dfSeries.csv')

test = df['name'].unique()
options = [{'label': t, 'value': t} for t in test]

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=options,
        value='',
        multi = True
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)