import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import sys
import os
import pandas as pd 


app = dash.Dash('app_name')

df_series = pd.read_csv('dfSeries.csv')

df_prepared=df_series
df_prepared = df_prepared.drop('episodes', axis=1)
df_prepared = df_prepared.drop('anime_id', axis=1)
df_prepared = df_prepared.drop('Classification', axis=1)


test = df_series['name'].unique()
options = [{'label': t, 'value': t} for t in test]

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=options,
        value='',
        multi = True,
        placeholder="Select one or more animes"
    ),
    html.Br(),
    html.Br(),
    html.Div(id='my-output'),

])

def fusion(first,second):
    fusiondf = first
    name = first.iloc[0][0]
    name2 = second.iloc[0][0]
    rating = (float(first['rating']) + float(second['rating']))/2
    fusiondf['rating'] = rating
    members = (float(first['members']) + float(second['members']))/2
    fusiondf['members'] = members
    genreAdjustment(first,second,fusiondf)
    return fusiondf

def genreAdjustment(first,second,fusion):
    for column in first:
        if(column != 'name' and column != 'rating' and column != 'members'):
            fusion[column] = 1 if int(second[column]) == 1 or int(first[column]) == 1 else 0

def fusionByNameList(animeList):
    animeElement = df_prepared.loc[df_prepared['name'] == animeList[0]]
    animeElement['name'] = ""
    for name in animeList:
        secondElement = df_prepared.loc[df_prepared['name'] == name]
        animeElement = fusion(animeElement,secondElement)
    return animeElement

@app.callback(
    Output('my-output', 'children'),
    [Input('dropdown', component_property='value')]
)
def callback(current_options):
    if(current_options):
        return html.Div([
                generate_table(recommendation(fusionByNameList(current_options)))
            ])


def recommendation(x):
    import joblib
    knn = joblib.load("knn.joblib")
    x = x.drop('name',axis=1)
    x = x.drop('Unnamed: 0',axis=1)
    predicted_value = int(knn.predict(x))
    category=df_series[df_series.Classification == predicted_value]
    category = category.drop('Unnamed: 0',axis=1)
    return category.sort_values(by=['members','rating'], ascending=False)

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
    






if __name__ == '__main__':
    app.run_server(debug=True)