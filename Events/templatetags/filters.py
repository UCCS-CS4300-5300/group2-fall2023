from django import template
from django.utils.dateformat import format

register = template.Library()

@register.filter
def format_date_range(start_time, end_time):
    # if days are the same only return the one day
    if start_time.date() == end_time.date():
        start_date = format(start_time, "F jS, Y")
        return start_date
    else:
        # if years are the same only print year at end else print year in both spots
        if start_time.year == end_time.year:
            start_date = format(start_time, "F jS")
        else:
            start_date = format(start_time, "F jS, Y")
            end_date = format(end_time, "F jS, Y")
        return f"{start_date} - {end_date}"
