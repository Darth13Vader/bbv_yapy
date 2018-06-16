# coding=utf-8

import csv  # библиотека для работы с csv файлами
import os  # библиотека для работы с файловой системой


# web framework
from flask import Flask
from flask import render_template
from flask import request

from src.web.form_anayze import form
from src.model.predict_all import predict_all


# указываем путь к папке с вспомогательными файлами
RESOURCES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../resources')

# указываем путь к файлу со списком камер (формат csv, с заголовками)
# по умолчанию ./resources/cameras.csv
CAMERAS_PATH = os.path.join(RESOURCES_PATH, 'cameras.csv')

PRECIP = [('Нет осадков', 0), ('Дождь', 1), ('Снег', 1)]  # тип осадков
INTENS = [('Слабый', 1), ('Средний', 2), ('Сильный', 3)]  # интенсивность осадков

app = Flask(__name__)  # инициализируем Flask приложение

with open(CAMERAS_PATH, encoding='utf-8', newline='') as csvfile:  # загружаем список камер из csv файла
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')  # указываем разделитель и кавычки
    cameras = list(reader)  # создаем список словарей с ключами id, location


# Главная страница (указание параметров)
@app.route('/', methods=['GET', 'POST'])
def index():
    res = []
    if request.method == 'POST':
        print(dict(request.form))
        df = form(dict(request.form))
        print(df)
        if df.empty:
            res.append('Некорректные введенные данные!')
        else:
            result_df = predict_all(df)
            print(result_df) # Не могу ничего проверить, проблемы с predict
        # TODO Return results page

    return render_template('index.html', cameras_list=cameras, precip=PRECIP, intens=INTENS)