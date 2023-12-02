# CS 4300 Fall 2023 Group 2
# Harvestly
# Test Events Filters

""" Test Suite for Events Filter functionality"""

from django.test import TestCase
from django.utils import timezone
from django.utils.dateformat import format
from Events.templatetags.filters import format_date_range

class FiltersTestCase(TestCase):
    """ Test Cases for the Events filters """

    def test_same_year_date_range(self):
        """ Test filter handling when the start/end times are same year """
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(days=2)

        result = format_date_range(start_time, end_time)
        expected_result = f"{format(start_time, 'M jS')} - {format(end_time, 'M jS, Y')}"

        self.assertEqual(result, expected_result)

    def test_different_year_date_range(self):
        """ Test filter handling when the start/end times are different years """
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(days=365)

        result = format_date_range(start_time, end_time)
        expected_result = f"{format(start_time, 'M jS, Y')} - {format(end_time, 'M jS, Y')}"

        self.assertEqual(result, expected_result)
