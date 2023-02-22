import pandas as pd
from io import BytesIO

from django.db.models.functions import TruncMonth
from django.db.models import Min, Max, QuerySet
from weather_aggregation.models import WeatherData


def read_weather_file(bytes_file: BytesIO) -> list[dict]:
    data_frame = pd.read_csv(bytes_file)
    data_frame.rename(columns={'STATION': 'station', 'DATE': 'date', 'TAVG': 'temperature_avg',
                               'TMAX': 'temperature_max', 'TMIN': 'temperature_min'}, inplace=True)
    data_frame = data_frame.drop(columns=['TAVG_ATTRIBUTES', 'TMAX_ATTRIBUTES', 'TMIN_ATTRIBUTES', 'NAME'])
    return data_frame.to_dict('records')


def write_weather_file(data: list, city: str) -> None:
    data = filter(lambda values: True if not WeatherData.objects.filter(city=city,
                                                                        date=values['date']) else False, data)
    weather_objects = [WeatherData(**values, city=city) for values in data]
    WeatherData.objects.bulk_create(weather_objects)


def create_visual_table(city: str) -> QuerySet:
    queryset = WeatherData.objects.filter(city=city) \
        .annotate(month=TruncMonth('date')) \
        .values('month') \
        .annotate(min_temp=Min('temperature_avg'), max_temp=Max('temperature_avg')) \
        .values('month', 'min_temp', 'max_temp')\
        .order_by('date')
    return queryset
