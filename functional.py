from pycbrf.toolbox import ExchangeRates
import datetime


#  Функция отправляет запрос на сервис ЦБ РФ и возвращает курс рубля к доллару (в руб)
def conversion_dollar_to_ruble():
    data = datetime.datetime.now()  # сегодняшнее число
    rates = ExchangeRates(data)  # Извлекаем обменные курсы
    res_convert = rates['USD'].value  # Нас интересуют $ доллары

    return float(res_convert)


