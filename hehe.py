import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import time

class RealTimePlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Data Visualization")
        # self.root.attributes('-fullscreen', True)  # Во весь экран
        self.root.configure(background='darkgrey')  # Темно-серый фон

        # Создание стиля для темной темы
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background='darkgrey', foreground='white')
        style.configure("TNotebook.Tab", background='gray', foreground='white')

        # Создание вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Создаем три вкладки
        self.frames = []
        self.figures = []
        self.axes = []
        self.lines = []
        self.data = []

        for i in range(3):
            frame = ttk.Frame(self.notebook)
            frame.pack(fill=tk.BOTH, expand=True)
            self.frames.append(frame)

            fig, ax = plt.subplots(figsize=(12, 8))
            fig.patch.set_facecolor('darkgrey')  # Темно-серый фон для фигуры
            ax.set_facecolor('dimgray')  # Темно-серый фон для оси
            self.figures.append(fig)
            self.axes.append(ax)

            data = {'x': [], 'y': []}
            self.data.append(data)

            line, = ax.plot([], [], 'r-')
            self.lines.append(line)

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            self.notebook.add(frame, text=f'График {i+1}')

        self.start_time = time.time()
        self.update_plot()

    def update_plot(self):
        current_time = time.time() - self.start_time
        for i in range(3):
            self.data[i]['x'].append(current_time)
            self.data[i]['y'].append(random.uniform(-1, 1))  # Здесь можно обновлять данными из реального источника

            self.lines[i].set_data(self.data[i]['x'], self.data[i]['y'])
            self.axes[i].set_xlim(0, max(10, current_time))
            self.axes[i].relim()
            self.axes[i].autoscale_view(tight=True, scaley=True)

        for fig in self.figures:
            fig.canvas.draw()

        self.root.after(1000, self.update_plot)  # Обновление каждые 1000 миллисекунд (1 секунда)

    def on_exit(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimePlotApp(root)
    root.mainloop()

