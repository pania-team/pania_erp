
from django import template
import jdatetime
register = template.Library()


@register.filter
def persian_weekday(jdate):
    if not isinstance(jdate, jdatetime.date):
        try:
            jdate = jdatetime.date.fromgregorian(date=jdate)
        except:
            return ''
    weekdays = [
        'شنبه',
        'یکشنبه',
        'دوشنبه',
        'سه‌شنبه',
        'چهارشنبه',
        'پنج‌شنبه',
        'جمعه',
    ]

    return weekdays[jdate.weekday()]
