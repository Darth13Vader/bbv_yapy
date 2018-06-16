import requests, json
import datetime
from datetime import datetime
from bs4 import BeautifulSoup

'''
DEBUG MODE
Если режим отладки включен, то функция dprint работает, 
иначе отключается вывод в консоль
'''
def dprint(*values, sep=' ', end='\n'):
    if DEBUG:
        print(*values, sep=sep, end=end)

DEBUG = False


# ----- Exceptions -----
class YWeatherIncorrectRequestError(Exception):
    pass

class IncorrectDateError(Exception):
    # Неверная дата
    pass


class WeatherInfo:
    def __init__(self, temp: int, wind_speed: float, prec_type: int, prec_strength: float):
        # Температура
        self.temp = temp

        # Скорость ветра
        self.wind_speed = wind_speed

        # Осадки:
        #   0 — без осадков.
        #   1 — дождь.
        #   2 — дождь со снегом.
        #   3 — снег.
        self.prec_type = prec_type

        # Сила осадков:
        #   0 — без осадков.
        #   0.25 — слабый дождь/слабый снег.
        #   0.5 — дождь/снег.
        #   0.75 — сильный дождь/сильный снег.
        #   1 — сильный ливень/очень сильный снег.
        self.prec_strength = prec_strength

        self.format_data()

    def format_data(self):
        # Измениение формата данных для их соответствия с форматом таблицы данных
        if self.prec_type == 3:
            self.prec_type = 2

        if self.prec_strength == 0.25:
            self.prec_strength = 1
        elif self.prec_strength == 0.5:
            self.prec_strength = 2
        elif self.prec_strength in [0.75, 1]:
            self.prec_strength = 3

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        # Если есть осадки
        if self.prec_type != 0:
            # Вид осадков
            prec_name = ['', 'дождь', 'снег'][self.prec_type]
            # Сила осадков
            prec_str_strength = ['', 'слабый', 'умеренный', 'сильный'][int(self.prec_strength)]
            prec = f'{prec_str_strength} {prec_name}'
        else:
            prec = 'без осадков'
        return f'Температура {self.temp}°, ветер {self.wind_speed} м/с, {prec}'


class WeatherHandler:
    @staticmethod
    def get(address_lat: str = '43.243423',
            address_lon: str = '76.948125',
            date: datetime = datetime(2018, 6, 13, hour=15)) -> WeatherInfo:
        '''
        Функция, рекомандованная к запуску из сторонних программ
        Определяет способ выдачи информации о погоде (дата в промежутке от - до):
            1. Загрузить из БД (до сегодня)
            2. Точный прогноз из Я.Погоды на заданный час (Сегодня - 3 дня)
            3. Точный прогноз из Яндекс погоды на время суток (4 дня - неделя)
            4. Примерный прогноз из Яндекс погоды (неделя - месяц)
            5. Предсказать вероятную из Яндекс погоды (более месяца)
        Принимает координаты точки местности, для которой нужен прогноз,
        а так же дату (и возможно, час - для пункта 2 только
        :param address_lat: <str> - Широта местности
        :param address_lon: <str> - Долгота местности
        :param date: <datetime> - Дата, возможно указание часа для п. 2
        :return: Объект класса WeatherInfo
        '''

        # Вычисление разницы в днях между текущей датой и введенной
        today = datetime.today().date()
        today = datetime(today.year, today.month, today.day)
        date_delta_days = (date - today).days

        if 0 <= date_delta_days <= 3:
            return WeatherHandler.yw_for_hour(address_lat, address_lon, date)
        elif 3 < date_delta_days <= 6:
            return WeatherHandler.yw_for_timeofday(address_lat, address_lon, date)
        elif date_delta_days > 6:
            return WeatherHandler.yw_predict(address_lat, address_lon, date)
        else:
            pass

    @staticmethod
    def yw_for_hour(address_lat: str, address_lon: str, date: datetime) -> WeatherInfo:
        api_responce = WeatherHandler.yw_api_request(address_lat, address_lon)

        day_data = None
        for ind, element in enumerate(api_responce['forecasts']):
            if date.strftime('%Y-%m-%d') == element['date']:
                day_data = element
                break

        if day_data is None:
            day_data = api_responce['forecasts'][0]

        hour_data = None
        for ind, element in enumerate(day_data['hours']):
            if str(date.hour) == element['hour']:
                hour_data = element
                break

        # После получения словаря с данными выделим нужные поля
        temp = hour_data['temp']                    # Температура
        wind_speed = hour_data['wind_speed']        # Скорость ветра
        prec_type = hour_data['prec_type']          # Осадки
        prec_strength = hour_data['prec_strength']  # Сила осадков

        # Возврат объекта с информацией о погоде
        return WeatherInfo(temp, wind_speed, prec_type, prec_strength)

    @staticmethod
    def yw_for_timeofday(address_lat: str, address_lon: str, date: datetime) -> WeatherInfo:
        if date.hour in [0, 1, 2, 3, 4, 5]:
            timeofday = 'night'
        elif date.hour in [6, 7, 8, 9, 10, 11]:
            timeofday = 'morning'
        elif date.hour in [12, 13, 14, 15, 16, 17]:
            timeofday = 'day'
        elif date.hour in [18, 19, 20, 21, 22, 23]:
            timeofday = 'evening'
        else:
            raise Exception()

        api_responce = WeatherHandler.yw_api_request(address_lat, address_lon)

        day_data = None
        for ind, element in enumerate(api_responce['forecasts']):
            if date.strftime('%Y-%m-%d') == element['date']:
                day_data = element
                break

        day_part_data = day_data['parts'][timeofday]

        # После получения словаря с данными выделим нужные поля
        temp = day_part_data['temp_avg']                # Температура
        wind_speed = day_part_data['wind_speed']        # Скорость ветра
        prec_type = day_part_data['prec_type']          # Осадки
        prec_strength = day_part_data['prec_strength']  # Сила осадков

        # Возврат объекта с информацией о погоде
        return WeatherInfo(temp, wind_speed, prec_type, prec_strength)

    @staticmethod
    def yw_predict(address_lat: str, address_lon: str, date: datetime) -> WeatherInfo:
        today = datetime.today()
        if date.month != today.month:
            month = ['january', 'february', 'march', 'april', 'may',
                     'june', 'july', 'august', 'september', 'october',
                     'november', 'december'][date.month - 1]
        else:
            month = ''

        soup = WeatherHandler.yw_raw_request(address_lat, address_lon, month)

        this_day = date.day
        this_month = ['января', 'февраля', 'марта', 'апреля',
                      'мая', 'июня', 'июля', 'августа',
                      'сентября', 'октября', 'ноября', 'декабря'][date.month - 1]
        dayname_required = f'{this_day} {this_month}'

        day_data = None

        rows = soup.find_all('div', {'class': 'climate-calendar__row'})
        for row in rows:
            days_list = row.find_all('div', {'class': 'climate-calendar__cell'})
            for day in days_list:
                day_name = day.find('h6', {'class': 'climate-calendar-day__detailed-day'})
                if day_name is None:
                    continue
                day_name = day_name.text
                if day_name.startswith(dayname_required):
                    day_data = day
                    break

        if day_data is None:
            pass
        else:
            temp_day = day_data.find('div', {'class': 'temp climate-calendar-day__detailed-basic-temp-day'}).text
            temp_day = int(temp_day[:-1].replace('−', '-'))
            temp_night = day_data.find('div', {'class': 'temp climate-calendar-day__detailed-basic-temp-night'}).text
            temp_night = int(temp_night[:-1].replace('−', '-'))

            if date.hour in [0, 1, 2, 3, 4, 5]:
                temp = temp_night
            elif date.hour in [6, 7, 8, 9, 10, 11]:
                temp = (temp_day + temp_night) // 2
            elif date.hour in [12, 13, 14, 15, 16, 17]:
                temp = temp_day
            elif date.hour in [18, 19, 20, 21, 22, 23]:
                temp = (temp_day + temp_night) // 2
            else:
                raise Exception()

            wind_speed = day_data.find('span', {'class': 'wind-speed'})
            if wind_speed is None:
                wind_speed = 0
            else:
                wind_speed = wind_speed.text

            # Ниже - определение типа осадков и их силы по иконке
            # Да, Гоша, ты верно думаешь
            # ЭТО. САМЫЙ. ГОВНОКОДИСТЫЙ. ГОВНОКОД МАТЬ ТВОЮ
            icon_types = {
                    # 1. Солнечно
                'icon icon_color_dark icon_thumb_skc-d icon_size_28 climate-calendar-day__detailed-basic-icon': (0, 0),
                    # 2. Облачно с прояснениями
                'icon icon_color_dark icon_thumb_bkn-d icon_size_28 climate-calendar-day__detailed-basic-icon': (0, 0),
                    # 3. Облачно
                'icon icon_color_dark icon_thumb_ovc icon_size_28 climate-calendar-day__detailed-basic-icon': (0, 0),
                    # 4. Облачно с прояснениями, небольшой дождь
                'icon icon_color_dark icon_thumb_bkn-m-ra-d icon_size_28 climate-calendar-day__detailed-basic-icon': (1, 0.25),
                    # 5. Облачно с прояснениями, сильный дождь
                'icon icon_color_dark icon_thumb_bkn-ra-d icon_size_28 climate-calendar-day__detailed-basic-icon': (1, 0.5),
                    # 6. Облачно, средний дождь
                'icon icon_color_dark icon_thumb_ovc-m-ra icon_size_28 climate-calendar-day__detailed-basic-icon': (1, 0.5),
                    # 7. Облачно, сильный дождь
                'icon icon_color_dark icon_thumb_ovc-ra icon_size_28 climate-calendar-day__detailed-basic-icon': (1, 0.75),
                    # 8. Облачно, средний снег
                'icon icon_color_dark icon_thumb_ovc-sn icon_size_28 climate-calendar-day__detailed-basic-icon': (3, 0.5)}

            prec_type, prec_strength = None, None
            for icon_type in icon_types.keys():
                is_it_here = day_data.find('i', {'class': icon_type})
                if is_it_here is None:
                    continue
                else:
                    prec_type, prec_strength = icon_types[icon_type]

            if prec_type is None:
                print('UNKNOWN ICON', day_data)
                raise Exception()

            return WeatherInfo(temp, wind_speed, prec_type, prec_strength)

    @staticmethod
    def yw_api_request(lat: str, lon: str) -> dict:
        url = f'https://api.weather.yandex.ru/v1/forecast?' \
              f'lat={lat}&lon={lon}' \
              f'&lang=ru_RU&limit=7&hours=true&extra=true'
        headers = {'X-Yandex-API-Key': 'c7dcbc12-1ccd-47ce-a1cf-8a837071ca91'}
        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            with open('resp.json', 'w', encoding='utf-8') as file:
                resp_json = json.loads(resp.content.decode('utf-8'))
                json.dump(resp_json, file)

            return resp_json
        else:
            raise YWeatherIncorrectRequestError(f'Url - {url}, content - {resp.content}')

    @staticmethod
    def yw_raw_request(lat: str, lon: str, month: str = '') -> BeautifulSoup:
        url = f'https://yandex.ru/pogoda/almaty/month/{month}?lat={lat}&lon={lon}'

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Connection': 'keep-alive',
                   'Cookie': 'yw_lc=162; yandexuid=1108336401528808425; i=YzCRuAWdGSQyqpk+FsxWCJ6tg1nrTIwtmTbomSlODgfKqIDoEk31zZY/fb9ToOJATzf0lWepjZ/fTC9lTlMB1ZiDqdQ=; yp=1844168428.yrtsi.1528808428#1560344431.zmblt.893; _ym_wasSynced=%7B%22time%22%3A1528808446078%2C%22params%22%3A%7B%22webvisor%22%3A%7B%22date%22%3A%222011-10-31%2016%3A20%3A50%22%7D%2C%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; mda=0; _ym_uid=1528808447328368953; _ym_isad=2; my=YwA=; _ym_visorc_115080=b',
                   'Host': 'yandex.ru',
                   'If-None-Match': 'W/"2d952-LrSgVRnoKATo999T+6k8nw"',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

        session = requests.Session()
        resp = session.get(url, headers=headers)

        soup = BeautifulSoup(resp.text, 'lxml')

        return soup


if __name__ == '__main__':
    print('=' * 60)

    print('Тест №1. Погода на сегодня')
    print(WeatherHandler.get())
    print('=' * 60)

    print('Тест №2. Погода на 14 июня на 17:00')
    print(WeatherHandler.get(date=datetime(2018, 6, 14, hour=17)))
    print('=' * 60)

    print('Тест №3. Погода на 18 июня на 23:00')
    print(WeatherHandler.get(date=datetime(2018, 6, 18, hour=23)))
    print('=' * 60)

    print('Тест №4. Погода на 24 июня на 4:00')
    print(WeatherHandler.get(date=datetime(2018, 6, 24, hour=4)))
    print('=' * 60)

    print('Тест №5. Погода на 20 августа днем')
    print(WeatherHandler.get(date=datetime(2018, 8, 20, hour=15)))
    print('=' * 60)

    print('Тест №6. Погода на 26 октября ночью')
    print(WeatherHandler.get(date=datetime(2018, 10, 26, hour=2)))
    print('=' * 60)

    print('Тест №7. Погода на 17 декабря к вечеру')
    print(WeatherHandler.get(date=datetime(2018, 12, 17, hour=23)))
    print('=' * 60)

    print('Тест №8. Погода на 3 марта 2019 утром')
    print(WeatherHandler.get(date=datetime(2019, 3, 3, hour=8)))
    print('=' * 60)

    # # HEADERS TEST
    # soup = WeatherHandler.yw_raw_request('43.243423', '76.948125')
    # data = soup.find('div', {'class': 'climate-graph i-bem'})
    # json_data = json.loads(data['data-bem'])
    # print(json_data['climate-graph']['graphData'][0])

