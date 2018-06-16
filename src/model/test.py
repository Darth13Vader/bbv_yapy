import pandas as pd
from predict_all import predict_all

test = pd.read_csv('clear_data2.csv')
to_predict = test.drop(['amount', 'point', 'speed', 'load'], axis=1)
result = predict_all(to_predict)

# result.to_csv('result.csv', index=False)

diff = result['point'] - test['point']
print(len(diff[abs(diff) > 1])/len(test['point']))
# print(result['amount'] ** 2 - test['amount'] ** 2)

