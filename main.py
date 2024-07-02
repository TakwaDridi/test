from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd

besoins = pd.read_excel("./data/L4 - Recueil des besoins envoyés - BU .xlsx", sheet_name="Liste besoin")

besoins = besoins.map(lambda x: x.strip() if isinstance(x, str) else x)
besoins['Gagné'] = besoins['Gagné'].replace(['En cours', 'En cous', 'En cousrs'], 'En cours')


fig1 = px.histogram(besoins, x='Secteur', color='Client')
fig2 = px.histogram(besoins, x='Secteur', color='Gagné')
fig3 = px.histogram(besoins, x='Semaine', color='Secteur')
app = Dash()

app.layout = html.Div(children=[
    html.H1(children='Recueil des besoins envoyés', style={'textAlign':'center'}),
    #dash_table.DataTable(data=besoins, page_size=10),
    #dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='clients par secteur', figure=fig1),
    dcc.Graph(id='status par secteur', figure=fig2),
    dcc.Graph(id='secteur par semaine', figure=fig3)
]
)

#@callback(
#    Output('graph-content', 'figure'),
#    Input('dropdown-selection', 'value')
#)
#def update_graph(value):
#    dff = df[df.country==value]
#    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run_server(debug=True)