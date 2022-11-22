import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import sys
import os
import pandas as pd 

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                generate_card_grid(recommendation(fusionByNameList(current_options)))
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
    
def generate_card_grid(dataframe, max_rows=10):
    return html.Div([
                (dbc.Card(
                    [
                        dbc.CardHeader(dataframe.iloc[i]['name'] , className="card-title"),
                        dbc.CardBody(
                            [
                                html.Div(
                                    "Episodes: " + str(dataframe.iloc[i]['episodes']),
                                    className="card-text",
                                ),
                                html.Div(
                                    "Rating: " + str(dataframe.iloc[i]['rating']),
                                    className="card-text",
                                ),
                                html.Div(
                                    "Members: " + str(dataframe.iloc[i]['members']),
                                    className="card-text",
                                ),
                                html.Div(
                                    "Genres: " + showGenres(dataframe.iloc[i]),
                                ),
                                dbc.Button("Go watch", color="primary"),
                            ]
                        ),     

                    ],
                    style={"width": "18rem"},
                )) for i in range(min(len(dataframe), max_rows))
            ], className="d-flex row")

""" def showGenres (dataframe):
    genres = []
    if (int(dataframe['Comedy']) == 1):
        genres.append(dbc.ListGroupItem("Comedy", color="info", class_name='h-50'))
    if (int(dataframe['Action']) == 1):
        genres.append(dbc.ListGroupItem("Action", color="info", class_name='h-25'))
    if (int(dataframe['Adventure']) == 1):
        genres.append(dbc.ListGroupItem("Adventure", color="info", class_name='h-25'))
    if (int(dataframe['Sci-Fi']) == 1):
        genres.append(dbc.ListGroupItem("Sci-Fi", color="info", class_name='h-25'))
    if (int(dataframe["Fantasy"]) == 1):
        genres.append(dbc.ListGroupItem("Fantasy", color="info", class_name='h-25'))
    if (int(dataframe['Shounen']) == 1):
        genres.append(dbc.ListGroupItem("Shounen", color="info", class_name='h-25'))
    if (int(dataframe['Romance']) == 1):
        genres.append(dbc.ListGroupItem("Romance", color="info", class_name='h-25'))
    if (int(dataframe['Drama']) == 1):
        genres.append(dbc.ListGroupItem("Drama", color="info", class_name='h-25'))
    if (int(dataframe['Supernatural']) == 1):
        genres.append(dbc.ListGroupItem("Supernatural", color="info", class_name='h-25'))
    if (int(dataframe['Magic']) == 1):
        genres.append(dbc.ListGroupItem("Magic", color="info", class_name='h-25'))
    if (int(dataframe['Kids']) == 1):
        genres.append(dbc.ListGroupItem("Kids", color="info", class_name='h-25'))
    return genres """

def showGenres (dataframe):
    genres = ""
    if (int(dataframe['Comedy']) == 1):
        genres += "Comedy, "
    if (int(dataframe['Action']) == 1):
        genres += "Action, "
    if (int(dataframe['Adventure']) == 1):
        genres += "Adventure, "
    if (int(dataframe['Sci-Fi']) == 1):
        genres += "Sci-Fi, "
    if (int(dataframe["Fantasy"]) == 1):
        genres += "Fantasy, "
    if (int(dataframe['Shounen']) == 1):
        genres += "Shounen, "
    if (int(dataframe['Romance']) == 1):
        genres += "Romance, "
    if (int(dataframe['Drama']) == 1):
        genres += "Drama, "
    if (int(dataframe['Supernatural']) == 1):
        genres += "Supernatural, "
    if (int(dataframe['Magic']) == 1):
        genres += "Magic, "
    if (int(dataframe['Kids']) == 1):
        genres += "Kids, "
    return genres


if __name__ == '__main__':
    app.run_server(debug=True)