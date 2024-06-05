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

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.x_data = []
        self.y_data = []

        self.line, = self.ax.plot(self.x_data, self.y_data, 'r-')
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-1, 1)

        self.update_plot()

    def update_plot(self):
        current_time = time.time()
        self.x_data.append(current_time)
        self.y_data.append(random.uniform(-1, 1))  # Здесь можно обновлять данными из реального источника

        # Обновляем диапазон оси x
        if current_time - self.x_data[0] > 10:
            self.ax.set_xlim(current_time - 10, current_time)

        self.line.set_data(self.x_data, self.y_data)
        self.ax.relim()
        self.ax.autoscale_view()

        self.canvas.draw()
        self.root.after(1000, self.update_plot)  # Обновление каждые 1000 миллисекунд (1 секунда)

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimePlotApp(root)
    root.mainloop()

