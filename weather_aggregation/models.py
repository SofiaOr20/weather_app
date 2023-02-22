from django.db import models


class WeatherData(models.Model):
    station = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    date = models.DateField()
    temperature_avg = models.FloatField(blank=True, null=True)
    temperature_min = models.FloatField(blank=True, null=True)
    temperature_max = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.date.strftime('%d.%m.%Y')

    # def save(self, *args, **kwargs):
    #     city, date = getattr(self, 'city'), getattr(self, 'date')
    #     if not WeatherData.objects.filter(city=city, date=date).exists():
    #         super(WeatherData, self).save(*args, **kwargs)
