import pandas as pd


def f_to_c(ft):
    return round((ft - 32) * (5 / 9))


# Перевод скорости ветра в м/c
def kt_to_ms(kt):
    return round(kt * 0.5)


# Определение типа осадков
def precipitation(code):
    # precip
    # 0 - нет осадков
    # 1 - дождь
    # 2 - снег
    # 3 - гроза
    # 4 - туман
    # 5 - дымка
    if code == 'M':
        return 0
    if 'RA' or 'SH' in code:
        return 1
    if 'SN' or 'SG' in code:
        return 2
    # Далее закомментировано, так как у Коли в коде нет таких погодных условий
    # if 'TS' in code:
    #    return 3
    # if 'BR' or 'FG' in code:
    #    return 4
    # if 'FU' in code:
    #    return 5
    return 1


# Интенсивность осадков
def intensity(code):
    # intensity
    # 0 - осадков нет
    # 1 - слабая
    # 2 - средняя
    # 3 - сильная
    if code == 'M':
        return 0
    if '-' in code:
        return 1
    if '+' in code:
        return 3
    return 2


# Считываем таблицу в DataFrame
data = pd.read_csv("new_weather.csv")
date = data['valid']  # Выделяем колонку для дальнейшей обработки
data = data.drop(['valid'], axis=1)  # Убираем лишнюю колонку

# Сплитим каждую строчку столбца по пробелу, образуем новый DataFrame
df = pd.DataFrame(date.str.split(' ', 0).tolist(), columns=['date', 'time'])

# Создаем новые колонки под наши нужды, чтобы не использовать кучу раз split
df['time'] = df['time'].str.split(':')  # Сплитим время по двоеточию
df['date'] = df['date'].str.split('-')  # Сплитим дату по тире


# Создаем колонки с нужной информацией
data['month'] = pd.to_numeric(df['date'].str[1])  # Выбираем индекс с месяцем и записываем в отдельный столбец
data['day'] = pd.to_numeric(df['date'].str[2])    # Выбираем индекс с днем и записываем в отдельный столбец
data['hour'] = pd.to_numeric(df['time'].str[0])   # Выбираем индекс с часом и записываем в отдельный столбец

# Берем колонки для будущей сортировки
data['year'] = pd.to_numeric(df['date'].str[0])
data['minute'] = pd.to_numeric(df['time'].str[1])

# Применяем функции к столбцам
data['temperature'] = pd.to_numeric(data.tmpf).apply(f_to_c)
data = data.drop(['tmpf'], axis=1)

data['sknt'] = data.sknt.apply(kt_to_ms)

data['precipitation'] = data.wxcodes.apply(precipitation)
data['intesity'] = data.wxcodes.apply(intensity)
data = data.drop(['wxcodes'], axis=1)

data = pd.concat([data], ignore_index=True)  # Генерируем 30 записей и сортируем
data = data.sort_values(by=['year', 'month', 'day', 'hour', 'minute'])
data = data.drop(['year', 'minute'], axis=True)

# Читаем основной дамп
main_data = pd.read_csv('clear_data.csv')

# Склеиваем дампы
result = pd.merge(data, main_data, how='inner', on=['month', 'day', 'hour'])
result.to_csv('data_with_weather.csv', index=False)
