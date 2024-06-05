import pandas as pd
import glob

# Укажите путь к вашим CSV-файлам. Используем glob для поиска всех файлов с расширением .csv в указанной директории.
file_paths = glob.glob('path_to_your_csv_files/*.csv')

# Считаем все CSV-файлы в список DataFrame
dfs = [pd.read_csv(file) for file in file_paths]

# Объединяем все DataFrame в один
combined_df = pd.concat(dfs, ignore_index=True)

# Сохраняем объединенный DataFrame в новый CSV-файл
combined_df.to_csv('combined_data.csv', index=False)

print(combined_df)
