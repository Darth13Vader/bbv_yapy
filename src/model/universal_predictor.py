#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
RU:
Функция с машинным обучением для предсказаний, написанная Дином Дмитрием

EN:
The function with machine learning for the predictions written by Din Dmitriy
"""


def predict(df, model_name, key):
    from catboost import CatBoostRegressor
    import pandas as pd

    model = CatBoostRegressor()  # Инициализируем модель
    model.load_model(model_name)
    return pd.DataFrame({key: model.predict(df)})  # Предсказываем
