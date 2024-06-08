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

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import gradio as gr
import matplotlib.pyplot as plt

# Загрузка данных
data = pd.read_csv('your_dataset.csv')

# Предобработка данных
data['date'] = pd.to_datetime(data['date'])
data = data.drop(columns=['note', 'stop_id'])
label_encoders = {}
categorical_columns = ['line', 'station', 'entry_name', 'line_name', 'station_name']
for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

X = data.drop(columns=['num_val'])
y = data['num_val']
y_binned = pd.qcut(y, q=3, labels=['низкая', 'средняя', 'высокая'])
X_train, X_test, y_train, y_test = train_test_split(X, y_binned, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

def predict_future(station_name):
    station_id = label_encoders['station_name'].transform([station_name])[0]
    future_dates = pd.date_range(start=data['date'].max(), periods=24, freq='M')
    future_data = pd.DataFrame({
        'date': future_dates,
        'hour': np.random.choice(data['hour'], size=24),
        'line': np.random.choice(data['line'], size=24),
        'station': station_id,
        'entry_name': np.random.choice(data['entry_name'], size=24),
        'line_name': np.random.choice(data['line_name'], size=24),
        'station_name': station_id,
        # Добавьте сюда все остальные необходимые атрибуты
    })
    future_predictions = model.predict(future_data)
    future_data['predicted_num_val'] = future_predictions

    plt.figure(figsize=(10, 5))
    plt.plot(future_data['date'], future_data['predicted_num_val'], marker='o')
    plt.title(f'Прогноз загруженности для станции {station_name} на два года вперед')
    plt.xlabel('Дата')
    plt.ylabel('Загруженность')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('/mnt/data/future_plot.png')
    return '/mnt/data/future_plot.png'

def predict_current(station_name):
    station_id = label_encoders['station_name'].transform([station_name])[0]
    current_data = data[data['station_name'] == station_id].tail(1)
    current_prediction = model.predict(current_data.drop(columns=['num_val']))
    return f'Текущая загруженность станции {station_name}: {current_prediction[0]}'

with gr.Blocks() as demo:
    with gr.Tab("Прогноз на два года"):
        station_input = gr.inputs.Textbox(label="Введите название станции")
        future_output = gr.outputs.Image(label="Прогноз загруженности")
        gr.Interface(fn=predict_future, inputs=station_input, outputs=future_output).launch(share=True)
    with gr.Tab("Текущая загруженность"):
        station_input = gr.inputs.Textbox(label="Введите название станции")
        current_output = gr.outputs.Textbox(label="Текущая загруженность")
        gr.Interface(fn=predict_current, inputs=station_input, outputs=current_output).launch(share=True)

demo.launch()
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import gradio as gr
import matplotlib.pyplot as plt

# Загрузка данных
data = pd.read_csv('your_dataset.csv')

# Предобработка данных
data['date'] = pd.to_datetime(data['date'])
data = data.drop(columns=['note', 'stop_id'])
label_encoders = {}
categorical_columns = ['line', 'station', 'entry_name', 'line_name', 'station_name']
for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

X = data.drop(columns=['num_val'])
y = data['num_val']
y_binned = pd.qcut(y, q=3, labels=['низкая', 'средняя', 'высокая'])
X_train, X_test, y_train, y_test = train_test_split(X, y_binned, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

def predict_future(station_name):
    station_id = label_encoders['station_name'].transform([station_name])[0]
    future_dates = pd.date_range(start=data['date'].max(), periods=24, freq='M')
    future_data = pd.DataFrame({
        'date': future_dates,
        'hour': np.random.choice(data['hour'], size=24),
        'line': np.random.choice(data['line'], size=24),
        'station': station_id,
        'entry_name': np.random.choice(data['entry_name'], size=24),
        'line_name': np.random.choice(data['line_name'], size=24),
        'station_name': station_id,
        'input_doors_count': np.random.choice(data['input_doors_count'], size=24),
        'input_doors_bandwidth': np.random.choice(data['input_doors_bandwidth'], size=24),
        'input_doors_total_bandwidth': np.random.choice(data['input_doors_total_bandwidth'], size=24),
        'input_turnstile_count': np.random.choice(data['input_turnstile_count'], size=24),
        'input_turnstile_bandwidth': np.random.choice(data['input_turnstile_bandwidth'], size=24),
        'input_turnstile_total_bandwidth': np.random.choice(data['input_turnstile_total_bandwidth'], size=24),
        'input_stairs_width': np.random.choice(data['input_stairs_width'], size=24),
        'input_stairs_bandwidth': np.random.choice(data['input_stairs_bandwidth'], size=24),
        'input_stairs_total_bandwidth': np.random.choice(data['input_stairs_total_bandwidth'], size=24),
        'input_escalator_count': np.random.choice(data['input_escalator_count'], size=24),
        'input_escalator_bandwidth': np.random.choice(data['input_escalator_bandwidth'], size=24),
        'input_escalator_total_bandwidth': np.random.choice(data['input_escalator_total_bandwidth'], size=24),
        'output_doors_count': np.random.choice(data['output_doors_count'], size=24),
        'output_doors_bandwidth': np.random.choice(data['output_doors_bandwidth'], size=24),
        'output_doors_total_bandwidth': np.random.choice(data['output_doors_total_bandwidth'], size=24),
        'output_turnstile_count': np.random.choice(data['output_turnstile_count'], size=24),
        'output_turnstile_bandwidth': np.random.choice(data['output_turnstile_bandwidth'], size=24),
        'output_turnstile_total_bandwidth': np.random.choice(data['output_turnstile_total_bandwidth'], size=24),
        'output_stairs_width': np.random.choice(data['output_stairs_width'], size=24),
        'output_stairs_bandwidth': np.random.choice(data['output_stairs_bandwidth'], size=24),
        'output_stairs_total_bandwidth': np.random.choice(data['output_stairs_total_bandwidth'], size=24),
        'output_escalator_count': np.random.choice(data['output_escalator_count'], size=24),
        'output_escalator_bandwidth': np.random.choice(data['output_escalator_bandwidth'], size=24),
        'output_escalator_total_bandwidth': np.random.choice(data['output_escalator_total_bandwidth'], size=24)
    })
    future_predictions = model.predict(future_data)
    future_data['predicted_num_val'] = future_predictions

    plt.figure(figsize=(10, 5))
    plt.plot(future_data['date'], future_data['predicted_num_val'], marker='o')
    plt.title(f'Прогноз загруженности для станции {station_name} на два года вперед')
    plt.xlabel('Дата')
    plt.ylabel('Загруженность')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('/mnt/data/future_plot.png')
    return '/mnt/data/future_plot.png'

def predict_current(station_name):
    station_id = label_encoders['station_name'].transform([station_name])[0]
    current_data = data[data['station_name'] == station_id].tail(1)
    current_prediction = model.predict(current_data.drop(columns=['num_val']))
    return f'Текущая загруженность станции {station_name}: {current_prediction[0]}'

with gr.Blocks() as demo:
    with gr.Tab("Прогноз на два года"):
        station_input = gr.inputs.Textbox(label="Введите название станции")
        future_output = gr.outputs.Image(label="Прогноз загруженности")
        gr.Interface(fn=predict_future, inputs=station_input, outputs=future_output).launch(share=True)
    with gr.Tab("Текущая загруженность"):
        station_input = gr.inputs.Textbox(label="Введите название станции")
        current_output = gr.outputs.Textbox(label="Текущая загруженность")
        gr.Interface(fn=predict_current, inputs=station_input, outputs=current_output).launch(share=True)

demo.launch()
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Выделение признаков и целевой переменной
X = data.drop(columns=['station', 'date', 'hour', 'line', 'line_id', 'line_name', 'station_id', 'station_name', 'entry_id', 'entry_name', 'note', 'stop_id'])
y = data['num_val']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели классификации (пример с RandomForestClassifier)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Оценка точности модели
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
