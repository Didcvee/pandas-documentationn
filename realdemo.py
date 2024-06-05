import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import datetime


# Генерация обманных данных
def generate_fake_data(cluster, station, period):
    np.random.seed(42)
    dates = [datetime.date.today() + datetime.timedelta(days=i) for i in range(period)]
    load = np.random.rand(period) * 100
    return dates, load


# Функция для отображения графика загруженности
def plot_load(cluster, station, period):
    dates, load = generate_fake_data(cluster, station, period)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, load, label=f'Cluster {cluster}, Station {station}')
    plt.xlabel('Date')
    plt.ylabel('Load')
    plt.title(f'Load Forecast for Cluster {cluster}, Station {station}')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    return plt


# Функция для отображения прогноза для выбранного кластера и периода
def forecast_cluster_period(cluster, period):
    dates, load = generate_fake_data(cluster, "All", period)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, load, label=f'Cluster {cluster}')
    plt.xlabel('Date')
    plt.ylabel('Load')
    plt.title(f'Forecast for Cluster {cluster}')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    return plt


# Функция для отображения прогноза для всех кластеров
def forecast_all_clusters(period):
    plt.figure(figsize=(10, 5))
    for cluster in range(1, 4):
        dates, load = generate_fake_data(cluster, "All", period)
        plt.plot(dates, load, label=f'Cluster {cluster}')

    plt.xlabel('Date')
    plt.ylabel('Load')
    plt.title(f'Forecast for All Clusters')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    return plt


# Создание интерфейса Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Load Forecasting Application")

    with gr.Tab("Cluster Station Load"):
        with gr.Row():
            cluster = gr.Dropdown(choices=[1, 2, 3], label="Cluster")
            station = gr.Textbox(label="Station")
            period = gr.Slider(minimum=1, maximum=730, step=1, label="Period (days)")

        load_plot = gr.Plot()
        gr.Button("Show Load").click(plot_load, [cluster, station, period], load_plot)

    with gr.Tab("Forecast by Cluster and Period"):
        with gr.Row():
            cluster = gr.Dropdown(choices=[1, 2, 3], label="Cluster")
            period = gr.Slider(minimum=1, maximum=730, step=1, label="Period (days)")

        cluster_plot = gr.Plot()
        gr.Button("Show Forecast").click(forecast_cluster_period, [cluster, period], cluster_plot)

    with gr.Tab("Forecast for All Clusters"):
        period = gr.Slider(minimum=1, maximum=730, step=1, label="Period (days)")

        all_clusters_plot = gr.Plot()
        gr.Button("Show All Forecasts").click(forecast_all_clusters, period, all_clusters_plot)

    gr.Markdown("""
    ### User Guide
    - **Cluster Station Load**: Select a cluster, enter a station name, and choose a period to view the load forecast.
    - **Forecast by Cluster and Period**: Select a cluster and a period to view the forecast for the entire cluster.
    - **Forecast for All Clusters**: Choose a period to view forecasts for all clusters.
    """)

# Запуск приложения
demo.launch()

