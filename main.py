import clickhouse_connect

# Подключение к ClickHouse
client = clickhouse_connect.get_client(host='localhost', port=8123, username='', password='', database='main')

# Выполнение запроса
result = client.query('SELECT * FROM aloha LIMIT 100')

# Обработка результата
for row in result.result_rows:
    print(row)

# Пример вставки данных
data = [
    (1, 'example1'),
    (2, 'example2')
]

client.insert('aloha', data, column_names=['id', 'name'])

# Закрытие соединения (если необходимо)
client.close()
