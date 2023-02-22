import datetime

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from weather_aggregation.forms import DocumentForm, RecordUpdateForm
from analytics.data_process import *


def base(request):
    return render(request, 'home.html')


def upload_file(request):
    message = 'Upload as many files as you want!'
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            bytes_file = form.cleaned_data.get('file').file
            city = form.cleaned_data.get('city')
            data_file = read_weather_file(bytes_file)
            write_weather_file(data_file, city)
            return redirect('stat')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()

    context = {'form': form, 'message': message}
    return render(request, 'upload.html', context)


def get_statistic(request):
    # TODO: add city box
    city = request.GET.get('city', 'Rivne')
    years = WeatherData.objects.dates('date', 'year')
    group_month = create_visual_table(city)
    page = request.GET.get('page', 1)

    paginator = Paginator(years, 10)
    try:
        part = paginator.page(page)
    except PageNotAnInteger:
        part = paginator.page(1)
    except EmptyPage:
        part = paginator.page(paginator.num_pages)

    return render(request, 'stat.html', context={'years': part, 'data': group_month})


def get_month_weather(request):
    date = request.GET.get('date', None)
    if date:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        queryset = WeatherData.objects.filter(date__month=date.month, date__year=date.year)
    else:
        queryset = WeatherData.objects.none()
    return render(request, 'details.html', context={'weather': queryset, 'city': queryset.first().city})


def update_record(request):
    date = request.GET.get('date', None)
    message = f'Here you can update temperature value at {date}'
    if date:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    else:
        date = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
    weather = WeatherData.objects.filter(date=date).values('temperature_avg', 'temperature_max',
                                                           'temperature_min', 'date')
    if request.method == 'POST':
        form = RecordUpdateForm(request.POST)
        if form.is_valid():
            weather.update(**form.cleaned_data)
            return redirect(f'/details/?date={date.strftime("%Y-%m-%d")}')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = RecordUpdateForm(initial=weather.first())

    context = {'form': form, 'message': message}
    return render(request, 'update.html', context)
