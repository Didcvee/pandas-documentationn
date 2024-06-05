import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from clickhouse_driver import Client
import datetime

# Подключение к базе данных Clickhouse
client = Client(host='localhost', database='metro')

# Функция для получения данных из Clickhouse с учетом интервала
def fetch_data_with_interval(query, columns, start_date, end_date):
    formatted_query = query.format(start_date=start_date, end_date=end_date)
    print(f"Executing query: {formatted_query}")  # Debug output
    try:
        result = client.execute(formatted_query)
    except Exception as e:
        print(f"Error executing query: {e}")
        raise
    return pd.DataFrame(result, columns=columns)

# Создание Dash приложения
app = dash.Dash(__name__)

# SQL-запросы
queries = {
    "load_percentage": '''
        SELECT
            Station,
            SUM(Entries + Exits) AS Total_Load,
            MAX(SUM(Entries + Exits)) OVER () AS Max_Load,
            (SUM(Entries + Exits) / MAX(SUM(Entries + Exits)) OVER ()) * 100 AS Load_Percentage
        FROM metro.station
        WHERE Date >= '{start_date}' AND Date <= '{end_date}'
        GROUP BY Station
        ORDER BY Load_Percentage DESC;
    ''',
    "real_capacity": '''
        SELECT
            Station,
            MAX(Entries + Exits) AS Max_Capacity
        FROM metro.station
        WHERE Date >= '{start_date}' AND Date <= '{end_date}'
        GROUP BY Station
        ORDER BY Max_Capacity DESC;
    ''',
    "top_stations": '''
        SELECT
            Station,
            SUM(Entries + Exits) AS Total_Load
        FROM metro.station
        WHERE Date >= '{start_date}' AND Date <= '{end_date}'
        GROUP BY Station
        ORDER BY Total_Load DESC
        LIMIT 10;
    ''',
    "avg_passengers": '''
        SELECT
            Station,
            AVG(Entries + Exits) AS Average_Passengers
        FROM metro.station
        WHERE Date >= '{start_date}' AND Date <= '{end_date}'
        GROUP BY Station
        ORDER BY Average_Passengers DESC;
    '''
}

# Названия столбцов для каждого запроса
columns = {
    "load_percentage": ["Station", "Total_Load", "Max_Load", "Load_Percentage"],
    "real_capacity": ["Station", "Max_Capacity"],
    "top_stations": ["Station", "Total_Load"],
    "avg_passengers": ["Station", "Average_Passengers"]
}

# Получение списка станций
stations_query = "SELECT DISTINCT Station FROM metro.station ORDER BY Station;"
stations = client.execute(stations_query)
stations_list = [station[0] for station in stations]

# Макет приложения
app.layout = html.Div(children=[
    html.H1(children='Метро Аналитика'),

    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2023, 12, 31),
            display_format='YYYY-MM-DD'
        ),
        dcc.Dropdown(
            id='station-dropdown',
            options=[{'label': station, 'value': station} for station in stations_list],
            value=stations_list[0],
            clearable=False
        )
    ]),

    dcc.Graph(id='load-percentage-graph'),
    dcc.Graph(id='real-capacity-graph'),
    dcc.Graph(id='top-stations-graph'),
    dcc.Graph(id='avg-passengers-graph')
])


@app.callback(
    [Output('load-percentage-graph', 'figure'),
     Output('real-capacity-graph', 'figure'),
     Output('top-stations-graph', 'figure'),
     Output('avg-passengers-graph', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('station-dropdown', 'value')]
)
def update_graphs(start_date, end_date, selected_station):
    # Получение данных с учетом выбранного интервала
    load_percentage_data = fetch_data_with_interval(queries["load_percentage"], columns["load_percentage"], start_date,
                                                    end_date)
    real_capacity_data = fetch_data_with_interval(queries["real_capacity"], columns["real_capacity"], start_date,
                                                  end_date)
    top_stations_data = fetch_data_with_interval(queries["top_stations"], columns["top_stations"], start_date, end_date)
    avg_passengers_data = fetch_data_with_interval(queries["avg_passengers"], columns["avg_passengers"], start_date,
                                                   end_date)

    # Фильтрация данных для выбранной станции
    filtered_load_percentage_data = load_percentage_data[load_percentage_data['Station'] == selected_station]

    # Проверка данных перед созданием графиков
    print(f"Load Percentage Data: {load_percentage_data.head()}")  # Debug output
    print(f"Filtered Load Percentage Data: {filtered_load_percentage_data.head()}")  # Debug output
    print(f"Real Capacity Data: {real_capacity_data.head()}")  # Debug output
    print(f"Top Stations Data: {top_stations_data.head()}")  # Debug output
    print(f"Avg Passengers Data: {avg_passengers_data.head()}")  # Debug output

    # Создание графиков
    fig_load_percentage = px.bar(filtered_load_percentage_data, x='Station', y='Load_Percentage',
                                 title=f'Загруженность станции {selected_station} в процентах')
    fig_real_capacity = px.bar(real_capacity_data, x='Station', y='Max_Capacity',
                               title='Реальная пропускная способность станций')
    fig_top_stations = px.bar(top_stations_data, x='Station', y='Total_Load', title='Топ загруженных станций')
    fig_avg_passengers = px.bar(avg_passengers_data, x='Station', y='Average_Passengers',
                                title='Среднее количество пассажиров на станциях')

    return fig_load_percentage, fig_real_capacity, fig_top_stations, fig_avg_passengers


if __name__ == '__main__':
    app.run_server(debug=True)



