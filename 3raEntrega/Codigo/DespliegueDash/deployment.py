import dash
import dash_core_components as dcc
import dash_html_components as html
import sys
import os
import pandas as pd 


app = dash.Dash('app_name')

df = pd.read_csv('dfSeries.csv')

test = df['name'].unique()
options = [{'label': t, 'value': t} for t in test]

app.layout = dcc.Dropdown(
    options=options,
    searchable=True
    )

if __name__ == '__main__':
    app.run_server(debug=True)