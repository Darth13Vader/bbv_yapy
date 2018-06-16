import pandas as pd


# Считываем таблицу в DataFrame
data = pd.read_csv("telemetrika.csv", index_col='id')
date = data['date']  # Выделяем колонку для дальнейшей обработки
data = data.drop(['date', 'uid', 'image_name', 'time'], axis=1)  # Убираем лишние колонки

# Сплитим каждую строчку столбца по пробелу, образуем новый DataFrame
df = pd.DataFrame(date.str.split(' ', 0).tolist(), columns=['date', 'time'])

# Создаем новые колонки под наши нужды, чтобы не использовать кучу раз split
df['time'] = df['time'].str[:-3].str.split(':')    # Убираем символы +06, сплитим по двоеточию
df['date'] = df['date'].str.split('-')             # Сплитим дату по тире

# Создаем колонки с нужной информацией
df['month'] = pd.to_numeric(df['date'].str[1])     # Выбираем индекс с месяцем и записываем в отдельный столбец
df['day'] = pd.to_numeric(df['date'].str[2])       # Выбираем индекс с днем и записываем в отдельный столбец
df['hour'] = pd.to_numeric(df['time'].str[0])      # Выбираем индекс с часом и записываем в отдельный столбец
df['minute'] = pd.to_numeric(df['time'].str[1]) \
               + df['hour'] * 60                   # Выбираем индекс с минутой и и записываем в отдельный столбец

df = df.drop(['date', 'time'], axis=1)             # Убираем вспомогательные колонки

res = pd.concat([data, df], axis=1, join='inner')  # Соединяем датафреймы

res.to_csv('clear_data.csv', index=False)          # Сохраняем в csv
