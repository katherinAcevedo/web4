from dash import Dash, html, dash_table, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
#creamos el objeto de la aplicacion
app = Dash(__name__)
app.title = 'tablero de control'


# cargar los datos
df = pd.read_csv('superstore.csv',delimiter=';', parse_dates=['Order Date','Ship Date'])
df2 = df[
  ['Province', 'Sales', 'Customer Segment']
].groupby(['Province', 'Customer Segment'], as_index=False).sum('Sales')

print(df2.info())


# definir el Layout
app.layout = html.Div([
  html.H1('Tablero de control'),
 dcc.Tabs(id='tabs', value='tab-1',children=[
   dcc.Tab(label='Tabla de datos', value='tab-1'),
   dcc.Tab(label='Histograma', value='tab-2'),
   dcc.Tab(label='Scatter', value='tab-3'),
 ]),
  html.Div(id='contenido'),
])

@callback(Output('contenido', 'children'),Input('tabs', 'value'))
def actualizar(tab):
  if tab == 'tab-1':
    return dash_table.DataTable(data=df.to_dict('records'),page_size=12)

  elif tab == 'tab-2':
    return dcc.Graph(figure=px.histogram(df, x='Province', y='Sales',histfunc='avg'))
  else:
    return dcc.Graph(figure=px.scatter(df, x='Order Date', y='Sales',color='Customer Segment')),




# programa principal
if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)