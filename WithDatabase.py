import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from clickhouse_driver import Client

class RealTimePlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Data Visualization")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")  # Во весь экран
        self.root.configure(background='darkgrey')  # Темно-серый фон

        # Создание стиля для темной темы
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background='darkgrey', foreground='white')
        style.configure("TNotebook.Tab", background='gray', foreground='white')

        # Создание вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Инициализация клиента ClickHouse
        self.client = Client(host='localhost', database='test')  # Укажите ваш хост ClickHouse

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

    def fetch_data(self, table):
        query = f"SELECT count() FROM {table}"
        try:
            result = self.client.execute(query)
            return result[0][0] if result else 0
        except Exception as e:
            print(f"Error fetching data from {table}: {e}")
            return 0

    def update_plot(self):
        current_time = time.time() - self.start_time
        tables = ["example_table", "example_table", "example_table"]  # Укажите ваши таблицы

        new_data = False
        for i, table in enumerate(tables):
            count = self.fetch_data(table)
            print(f"Table {table} count: {count}")  # Лог для проверки данных

            if len(self.data[i]['y']) == 0 or count != self.data[i]['y'][-1]:
                new_data = True
                self.data[i]['x'].append(current_time)
                self.data[i]['y'].append(count)

                self.lines[i].set_data(self.data[i]['x'], self.data[i]['y'])
                self.axes[i].set_xlim(0, max(10, current_time))
                self.axes[i].relim()
                self.axes[i].autoscale_view(tight=True, scaley=True)

        if new_data:
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
