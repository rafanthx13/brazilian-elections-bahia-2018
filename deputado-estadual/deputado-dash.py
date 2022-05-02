import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json
# Nâo de o nome de 'dash.py' ao arquivo
# lembre-se de que eh diferente do jupytre para o aqruivo python: O inicio (app) e fim (port) do codigo

df_deputado_tse = pd.read_csv('./deputado_estadual_tse.csv', sep=';')
df_deputado_gazeta = pd.read_csv('./deputado_gazeta_info.csv', sep=';')
df_deputado_info =  pd.merge(
    df_deputado_tse, df_deputado_gazeta, how="inner", left_on='nrCandidato', right_on='Número'
)

# Build App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


app.layout = dbc.Container(
    children=[
        # Titulo e Info Input
        dbc.Row([
            dbc.Col([
                html.H1(children="DashBoard Eleições 2028 - Deputados Estaduais na Bahia"),
                html.P("Escolha o Deputado Estadual:", style={"margin-top": "40px"}),
                html.Div(
                        className="div-for-dropdown",
                        id="div-test",
                        children=[
                             dcc.Dropdown(df_deputado_info['Nome na urna'], '',
                                          id='deputado-dropdown'),
                        ],
                ),
                
            ]),
            dbc.Col([
                
                html.Div([
                    html.Img(id='hover-image', src='children', height=300)
                ], style={'paddingTop':35}),
                
                html.Div([
                            html.Span(id='nr-partido'),
                            html.Span(' - '),
                            html.Span(id='sigla-partido'),
                            html.Span(' - Número:'),
                            html.Span(id='nr-candidato')
                        ]),
               
                
            ]),
            dbc.Col([
                html.Div([
                            html.Span(id='idade'),
                            html.Span(' - '),
                            html.Span(id='ocupation'),
                            html.Span(' - Número:'),
                            html.Span(id='race-color'),
                            html.Span(' - '),
                             html.Span(id='total-recebido'),
                        
                    
                        ]),
                
            ])
        ]),
        
#         dbc.Row([]),
        
#         dbc.Row([]),
        
#         dbc.Row([]),
        
])

# =====================================================================
# Interactivity

def get_deputado_info(deputado_name):
    r = df_deputado_info[ df_deputado_info['Nome na urna'] == deputado_name]
    list_attrs_output = ['img', 'nrPartido', 'siglaPartido',
                         'totalRecebido', 'nrCandidato', 
                         'Idade', 'Ocupação', 'Cor/Raça']
    return tuple([r[el].iloc[0] for el in list_attrs_output])

# Change DropDown Option => Change Image
# Change DropDown Option => Change Image
@app.callback([
    Output('hover-image', 'src'),
    Output('nr-partido', 'children'),
    Output('sigla-partido', 'children'),
    Output('total-recebido', 'children'),
    Output('nr-candidato', 'children'),
    Output('idade', 'children'),
    Output('ocupation', 'children'),
    Output('race-color', 'children')],
    Input('deputado-dropdown', 'value') )
def callback_image(deputado_name):
    return get_deputado_info(deputado_name)






# Define callback to update graph
# @app.callback(
#     Output('graph', 'figure'),
#     [Input("colorscale-dropdown", "value")]
# )
# def update_figure(colorscale):
#     return px.scatter(
#         df, x="total_bill", y="tip", color="size",
#         color_continuous_scale=colorscale,
#         render_mode="webgl", title="Tips"
#     )
# Run app and display result inline in the notebook

if __name__ == "__main__":
    app.run_server(debug=True, port=8052)