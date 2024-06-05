import joblib

# Загрузка моделей с диска
lr_model_entry = joblib.load('models/lr_model_entry.pkl')
lr_model_exit = joblib.load('models/lr_model_exit.pkl')
gb_model_entry = joblib.load('models/gb_model_entry.pkl')
gb_model_exit = joblib.load('models/gb_model_exit.pkl')
xgb_model_entry = joblib.load('models/xgb_model_entry.pkl')
xgb_model_exit = joblib.load('models/xgb_model_exit.pkl')

models = {
    'lr': (lr_model_entry, lr_model_exit),
    'gb': (gb_model_entry, gb_model_exit),
    'xgb': (xgb_model_entry, xgb_model_exit)
}

import gradio as gr
import pandas as pd
import numpy as np
from datetime import timedelta


# Функция для прогнозирования
def forecast(models, model_name, start_date, periods, freq='H'):
    future_dates = pd.date_range(start_date, periods=periods, freq=freq)
    future_data = pd.DataFrame({
        'datetime': future_dates,
        'month': future_dates.month,
        'day': future_dates.day,
        'year': future_dates.year,
        'day_of_year': future_dates.dayofyear,
        'week_of_year': future_dates.isocalendar().week,
        'hour': future_dates.hour,
        'day_of_week': future_dates.dayofweek
    })

    # Удаление столбца datetime
    future_data = future_data.drop(columns=['datetime'])

    # Прогнозирование
    entry_forecast = models[model_name][0].predict(future_data)
    exit_forecast = models[model_name][1].predict(future_data)

    return future_dates, entry_forecast, exit_forecast


# Функция для интерфейса
def predict(cluster, station, model_name, start_date, periods):
    filtered_data = data[(data['Cluster'] == cluster) & (data['Station'] == station)]
    future_dates, entry_forecast, exit_forecast = forecast(models, model_name, start_date, periods)

    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Entries': entry_forecast,
        'Exits': exit_forecast
    })

    return forecast_df


# Интерфейс Gradio
def interface(cluster, station, model_name, start_date, periods):
    forecast_df = predict(cluster, station, model_name, start_date, periods)
    return forecast_df


# Список кластеров, станций и моделей
clusters = data['Cluster'].unique()
stations = data['Station'].unique()
model_names = ['lr', 'gb', 'xgb']

# Интерфейс Gradio
inputs = [
    gr.inputs.Dropdown(clusters, label="Select Cluster"),
    gr.inputs.Dropdown(stations, label="Select Station"),
    gr.inputs.Dropdown(model_names, label="Select Model"),
    gr.inputs.Date(label="Select Start Date", value="2024-06-01"),
    gr.inputs.Slider(minimum=1, maximum=24 * 365 * 2, step=24, label="Select Period (hours)")
]

outputs = gr.outputs.Dataframe()

# Запуск Gradio интерфейса
gr.Interface(fn=interface, inputs=inputs, outputs=outputs, description="Forecast of Subway Entries and Exits").launch()
