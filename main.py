from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd



template = 'plotly'
dropdown_dict = {
    'Client': 'Client',
    'Gagné': 'Gagné',
    'Reponse L4 au commerce': 'Reponse L4 au commerce'}
besoins = pd.read_excel("./data/L4 - Recueil des besoins envoyés - BU .xlsx", sheet_name="Liste besoin")

besoins = besoins.map(lambda x: x.strip() if isinstance(x, str) else x)
besoins['Gagné'] = besoins['Gagné'].replace(['En cours', 'En cous', 'En cousrs'], 'En cours')


fig1 = px.histogram(besoins, x='Secteur', color='Client', template=template)
fig2 = px.histogram(besoins, x='Secteur', color='Gagné', template=template)
fig3 = px.histogram(besoins, x='Semaine', color='Secteur', template=template)
fig4 = px.histogram(besoins, x='Semaine', color='Reponse L4 au commerce', template=template)
app = Dash()

app.layout = html.Div(children=[
    html.H1(children='Recueil des besoins envoyés', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': k, 'value': v}
            for k, v in dropdown_dict.items()
        ],
        value='Secteur',
    ),
    dcc.Graph(id='dropdown graph'),
    dcc.RangeSlider(
        id='week slider',
        min=besoins['Semaine'].min(),
        max=besoins['Semaine'].max(),
        step=1,
        marks={str(week): str(week) for week in besoins['Semaine'].unique()},
        value=[besoins['Semaine'].min(), besoins['Semaine'].min()]
    ),
    dcc.Graph(id='offres par semaine'),
    dcc.Graph(id='offres par secteur et par semaine')
]
)

@app.callback(
    Output('dropdown graph', 'figure'),
    Input('dropdown', 'value'))
def update_bar_chart(dim):
    df = besoins # replace with your own data source
    fig = px.histogram(
        df, x='Secteur', color=dim, template=template)
    return fig

@app.callback(
    Output('offres par semaine', 'figure'),
    Input('week slider', 'value'))
def update_figure(selected_weeks):
    df_1 = besoins.groupby(by=['Semaine', 'Secteur', 'BU']).size().reset_index(name="nb offres")
    filtered_df = df_1[df_1['Semaine'].between(min(selected_weeks), max(selected_weeks))]

    fig = px.scatter(filtered_df, x='Semaine', y="nb offres",
                     size="nb offres", color="Secteur", hover_name= 'BU',
                     size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('offres par secteur et par semaine', 'figure'),
    Input('week slider', 'value')
)
def update_figure(selected_weeks):
    df_1 = besoins.groupby(by=['Semaine', 'Secteur', 'BU', 'Client']).size().reset_index(name="nb offres")
    filtered_df = df_1[df_1['Semaine'].between(min(selected_weeks), max(selected_weeks))]

    fig = (px.histogram(
        filtered_df, x=filtered_df['Semaine'].astype(str),
        color='Secteur',template=template)
           .update_layout(xaxis_title = 'Semaine'
    ))

    fig.update_layout(transition_duration=500)

    return fig
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)