from django.test import TestCase
from django.utils import timezone
from Events.templatetags.filters import format_date_range
from django.utils.dateformat import format


class FiltersTestCase(TestCase):
    def test_same_year_date_range(self):
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(days=2)

        result = format_date_range(start_time, end_time)
        expected_result = f"{format(start_time, 'M jS')} - {format(end_time, 'M jS, Y')}"

        self.assertEqual(result, expected_result)

    def test_different_year_date_range(self):
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(days=365)

        result = format_date_range(start_time, end_time)
        expected_result = f"{format(start_time, 'M jS, Y')} - {format(end_time, 'M jS, Y')}"

        self.assertEqual(result, expected_result)