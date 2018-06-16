#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
RU:
Часть с машинным обучением модели для предсказания баллов, написанная Дином Дмитрием

EN:
The part with machine learning for predictions of point was written by Din Dmitriy
"""

import pandas as pd
from catboost import CatBoostRegressor


# Извлекаем данные из csv файла в DataFrame
data_frame = pd.read_csv("clear_data.csv")

x_train = data_frame.drop(['point', 'amount'], axis=1)
y_train = data_frame['point']

# Инициализируем модель (крутим параметры)
model = CatBoostRegressor(iterations=1000,
                          learning_rate=0.026,
                          depth=4,
                          l2_leaf_reg=None,
                          model_size_reg=None,
                          rsm=None,
                          loss_function='RMSE',
                          border_count=None,
                          feature_border_type=None,
                          fold_permutation_block_size=None,
                          od_pval=None,
                          od_wait=None,
                          od_type=None,
                          nan_mode=None,
                          counter_calc_method=None,
                          leaf_estimation_iterations=None,
                          leaf_estimation_method=None,
                          thread_count=10,
                          random_seed=None,
                          use_best_model=None,
                          verbose=None,
                          logging_level=None,
                          metric_period=None,
                          ctr_leaf_count_limit=None,
                          store_all_simple_ctr=None,
                          max_ctr_complexity=None,
                          has_time=None,
                          one_hot_max_size=None,
                          random_strength=None,
                          name=None,
                          ignored_features=None,
                          train_dir=None,
                          custom_metric=None,
                          eval_metric=None,
                          bagging_temperature=None,
                          save_snapshot=None,
                          snapshot_file=None,
                          fold_len_multiplier=None,
                          used_ram_limit=None,
                          gpu_ram_part=None,
                          allow_writing_files=None,
                          approx_on_full_history=None,
                          boosting_type=None,
                          simple_ctr=None,
                          combinations_ctr=None,
                          per_feature_ctr=None,
                          task_type=None,
                          device_config=None,
                          devices=None,
                          bootstrap_type=None,
                          subsample=None,
                          max_depth=None,
                          n_estimators=None,
                          num_boost_round=None,
                          num_trees=None,
                          colsample_bylevel=None,
                          random_state=None,
                          reg_lambda=None,
                          objective=None,
                          eta=None,
                          max_bin=None,
                          gpu_cat_features_storage=None,
                          data_partition=None)

model.fit(x_train, y_train)  # Обучаем модель
model.save_model('model_for_point')  # Сохраняем модель
