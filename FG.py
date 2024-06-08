import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Загрузка данных
data = pd.read_csv('data.csv', sep=';')
# Удаление ненужного столбца global_id
data = data.drop(columns=["Unnamed: 7"])
# Преобразование категориальных переменных в числовые
data['Line'] = pd.factorize(data['Line'])[0]
data['Quarter'] = pd.factorize(data['Quarter'])[0]

# Исключение ненужных столбцов
data = data.drop(['NameOfStation', 'global_id'], axis=1)

# Масштабирование данных
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# Применение PCA
pca = PCA()
pca.fit(scaled_data)

# Важность каждой компоненты
explained_variance_ratio = pca.explained_variance_ratio_

# Вывод результатов
print("Доля объясненной дисперсии для каждой компоненты:")
print(explained_variance_ratio)
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Загрузка данных
data = pd.read_csv('your_dataset.csv')

# Предобработка данных
# Преобразование дат в datetime формат
data['date'] = pd.to_datetime(data['date'])

# Удаление ненужных столбцов (если есть)
data = data.drop(columns=['note', 'stop_id'])

# Преобразование категориальных данных в числовые
label_encoders = {}
categorical_columns = ['line', 'station', 'entry_name', 'line_name', 'station_name']
for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Целевая переменная и признаки
X = data.drop(columns=['num_val'])
y = data['num_val']

# Биннинг целевой переменной (низкая, средняя, высокая загруженность)
y_binned = pd.qcut(y, q=3, labels=['низкая', 'средняя', 'высокая'])

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y_binned, test_size=0.2, random_state=42)

# Обучение модели
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))