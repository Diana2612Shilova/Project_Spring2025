import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv('allsolod.csv')
manufacturers = df['Производитель'].value_counts().reset_index()
manufacturers.columns = ['Производитель', 'Количество видов солода']
fig = px.bar(manufacturers, x="Производитель", y="Количество видов солода", title="Статистика по производителям солода")
df2 = pd.read_csv('khmel.csv')
fig2 = px.scatter(df2, x = 'Кислотность итоговая', y = 'Цена за килограмм', title="Кислотность vs цена хмеля")
avg_price = df.groupby('Производитель', as_index=False)['Цена за кг, руб'].mean()
fig3 = px.bar(avg_price, x='Производитель', y='Цена за кг, руб', title="Средняя цена солода за 1 кг по производителям")
app.layout = html.Div([
    dcc.Graph(id='bar-chart', figure=fig),
    dcc.Graph(id='scatter-plot', figure=fig2),
    dcc.Graph(id='bar-chart2', figure=fig3)
])
if __name__ == '__main__':
    app.run(debug=True)