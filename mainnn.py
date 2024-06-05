import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from clickhouse_driver import Client

# Подключение к базе данных Clickhouse
client = Client(host='localhost', database='metro')

# Функция для получения данных из Clickhouse с учетом выбранного интервала
def fetch_data_with_interval(query, columns, start_date, end_date):
    query = query.replace("{start_date}", start_date).replace("{end_date}", end_date)
    result = client.execute(query)
    return pd.DataFrame(result, columns=columns)

# Создание Dash приложения
app = dash.Dash(__name__)

# SQL-запросы (с подстановкой дат)
queries = {
    "load_percentage": '''
        SELECT
            Station,
            (SUM(Entries) + SUM(Exits)) AS Total_Load,
            MAX(SUM(Entries) + SUM(Exits)) OVER () AS Max_Load,
            ((SUM(Entries) + SUM(Exits)) / MAX(SUM(Entries) + SUM(Exits)) OVER ()) * 100 AS Load_Percentage
        FROM metro.station
        WHERE Date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY Station
        ORDER BY Load_Percentage DESC;
    ''',
    "real_capacity": '''
        SELECT
            Station,
            MAX(Entries + Exits) AS Max_Capacity
        FROM metro.station
        WHERE Date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY Station
        ORDER BY Max_Capacity DESC;
    ''',
    "top_stations": '''
        SELECT
            Station,
            SUM(Entries + Exits) AS Total_Load
        FROM metro.station
        WHERE Date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY Station
        ORDER BY Total_Load DESC
        LIMIT 10;
    ''',
    "avg_passengers": '''
        SELECT
            Station,
            AVG(Entries + Exits) AS Average_Passengers
        FROM metro.station
        WHERE Date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY Station
        ORDER BY Average_Passengers DESC;
    '''
}

# Названия столбцов для каждого запроса
columns = {
    "load_percentage": ["Station","Total_Load", "Max_Load", "Load_Percentage"],
    "real_capacity": ["Station", "Max_Capacity"],
    "top_stations": ["Station", "Total_Load"],
    "avg_passengers": ["Station", "Average_Passengers"]
}

# Создание графиков с пустыми данными
fig_load_percentage = px.bar(title='Загруженность станции в процентах')
fig_real_capacity = px.bar(title='Реальная пропускная способность станций')
fig_top_stations = px.bar(title='Топ загруженных станций')
fig_avg_passengers = px.bar(title='Среднее количество пассажиров на станциях')

# Макет приложения
app.layout = html.Div(children=[
    html.H1(children='Метро Аналитика'),

    dcc.DatePickerRange(
        id='date-range-picker',
        min_date_allowed='МИНИМАЛЬНАЯ ДАТА',  # Настройте минимальную дату
        max_date_allowed='МАКСИМАЛЬНАЯ ДАТА',  # Настройте максимальную дату
        initial_visible_month='НАЧАЛЬНЫЙ МЕСЯЦ',  # Настройте начальный видимый месяц
        start_date='НАЧАЛЬНАЯ ДАТА',  # Настройте начальную дату
        end_date='КОНЕЧНАЯ ДАТА'  # Настройте конечную дату
    ),

    dcc.Graph(
        id='load-percentage-graph',
        figure=fig_load_percentage
    ),

    dcc.Graph(
        id='real-capacity-graph',
        figure=fig_real_capacity
    ),

    dcc.Graph(
        id='top-stations-graph',
        figure=fig_top_stations
    ),

    dcc.Graph(
        id='avg-passengers-graph',
        figure=fig_avg_passengers
    ),
])

@app.callback(
    Output('load-percentage-graph', 'figure'),
    Output('real-capacity-graph', 'figure'),
    Output('top-stations-graph', 'figure'),
    Output('avg-passengers-graph', 'figure'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_graphs(start_date, end_date):
    load_percentage_data = fetch_data_with_interval(queries["load_percentage"], columns["load_percentage"], start_date, end_date)
    real_capacity_data = fetch_data_with_interval(queries["real_capacity"], columns["real_capacity"], start_date, end_date)
    top_stations_data = fetch_data_with_interval(queries["top_stations"], columns["top_stations"], start_date, end_date)
    avg_passengers_data = fetch_data_with_interval(queries["avg_passengers"], columns["avg_passengers"], start_date, end_date)

    fig_load_percentage = px.bar(load_percentage_data, x='Station', y='Load_Percentage', title='Загруженность станции в процентах')
    fig_real_capacity = px.bar(real_capacity_data, x='Station', y='Max_Capacity', title='Реальная пропускная способность станций')
    fig_top_stations = px.bar(top_stations_data, x='Station', y='Total_Load', title='Топ загруженных станций')
    fig_avg_passengers = px.bar(avg_passengers_data, x='Station', y='Average_Passengers', title='Среднее количество пассажиров на станциях')

    return fig_load_percentage, fig_real_capacity, fig_top_stations, fig_avg_passengers

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)



