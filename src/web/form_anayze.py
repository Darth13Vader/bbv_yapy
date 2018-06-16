from src.web.get_week_day import *
from src.web.weather import *
import pandas as pd


def form(f):
    result = dict()
    print(f)
    if not f['date'][0] or not f['time'][0]:
        return pd.DataFrame()

    result['bv_number'] = int(f['camera'][0][1])
    d, m, y = f['date'][0].split('.')
    day, month = int(d), int(m)
    strdate = '-'.join([y, m, d])
    result['month'] = [month]
    result['res_day'] = [int(is_holiday(strdate) or is_weekend(strdate))]
    result['weekday'] = [get_week_day(strdate)]

    h, m = f['time'][0][:5].split(':')
    result['hour'] = [int(h[1])] if h.startswith('0') else [int(h)]
    result['minute'] = [int(m[1])] if m.startswith('0') else [int(m)]

    if int(f['option'][0]):
        print(int(f['option'][0]))
        forecast = WeatherHandler.get(date=datetime(int(y), month, day))
        result['temp'] = [forecast.temp]
        result['precip'] = [forecast.prec_type]
        result['intensity'] = [forecast.prec_strength]
    else:
        if not f['temperature'][0] or 'precip' not in f:
            return pd.DataFrame()
        if f['precip'][0] == 'Нет осадков':
            result['intens'] = [0]
        else:
            if 'intens' not in f:
                result['intens'] = [1]
            elif not f['intens'][0]:
                result['intens'] = [1]

        result['temp'] = int(f['temperature'][0])
        result['precip'] = int(f['precip'][0])

    return pd.DataFrame(result)
