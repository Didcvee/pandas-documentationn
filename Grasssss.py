import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import time
import threading

# Функция для генерации нового графика
def generate_plot():
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x + time.time())
    plt.figure()
    plt.plot(x, y)
    plt.title("Динамический график")
    plt.xlabel("x")
    plt.ylabel("sin(x + t)")
    return plt.gcf()

# Функция для обновления графика
def update_plot():
    while True:
        gr.update(generate_plot())
        time.sleep(1)  # Обновляем график каждую секунду

# Создаем интерфейс Gradio
interface = gr.Interface(
    fn=generate_plot,
    inputs=None,
    outputs="plot",
    live=True
)

# Запускаем обновление графика в отдельном потоке
thread = threading.Thread(target=update_plot)
thread.start()

# Запускаем интерфейс
interface.launch()
