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
