from django import template

register = template.Library()


@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)


@register.filter()
def filter_month(data, month):
    return data.filter(date__month=month).order_by('date__year')


@register.filter()
def filter_year(data, years):
    queryset = []
    for year in years:
        current_value = data.filter(date__year=year.year)
        if current_value:
            queryset.append(current_value.values('month', 'min_temp', 'max_temp').first())
        else:
            queryset.append(None)
    return queryset


@register.filter()
def date_format(date):
    return date.strftime('%Y-%m-%d')
