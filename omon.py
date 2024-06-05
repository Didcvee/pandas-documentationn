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
        self.root.configure(background='#2e2e2e')  # Темно-серый фон

        # Создание стиля для темной темы
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background='#2e2e2e', foreground='white')
        style.configure("TNotebook.Tab", background='#4e4e4e', foreground='white')
        style.map("TNotebook.Tab", background=[("selected", "#1e1e1e")])

        # Создание заголовка
        header_frame = tk.Frame(self.root, bg='#1e1e1e')
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(header_frame, text="Real-Time Data Visualization", bg='#1e1e1e', fg='white', font=("Helvetica", 24))
        header_label.pack(pady=10)

        # Создание вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Инициализация клиента ClickHouse
        self.client = Client(host='localhost')  # Укажите ваш хост ClickHouse

        # Создаем три вкладки
        self.frames = []
        self.figures = []
        self.axes = []
        self.lines = []
        self.data = []
        self.graph_titles = ["Graph 1", "Graph 2", "Graph 3"]

        for i in range(3):
            frame = ttk.Frame(self.notebook)
            frame.pack(fill=tk.BOTH, expand=True)
            self.frames.append(frame)

            fig, ax = plt.subplots(figsize=(12, 8))
            fig.patch.set_facecolor('#2e2e2e')  # Темно-серый фон для фигуры
            ax.set_facecolor('#3e3e3e')  # Темно-серый фон для оси
            self.figures.append(fig)
            self.axes.append(ax)

            ax.set_title(self.graph_titles[i], color='white', fontsize=18)
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')

            ax.set_xlabel("Time (s)", color='white')
            ax.set_ylabel("Count", color='white')

            data = {'x': [], 'y': []}
            self.data.append(data)

            line, = ax.plot([], [], 'r-', linewidth=2)
            self.lines.append(line)

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

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
            return None  # Вернуть None в случае ошибки

    def update_plot(self):
        current_time = time.time() - self.start_time
        tables = ["table1", "table2", "table3"]  # Укажите ваши таблицы

        new_data = False
        for i, table in enumerate(tables):
            count = self.fetch_data(table)
            if count is None:  # Если произошла ошибка при получении данных
                continue

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
