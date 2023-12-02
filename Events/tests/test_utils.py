### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Events Utilities

""" Test Suite for Google Maps API Utilities"""

from unittest.mock import patch
from django.conf import settings
from django.test import TestCase
from Events import utils

class UtilsTests(TestCase):
    """ Test cases for Google Maps API Utilities """

    def test_get_coordinates_success(self):
        """Test get_coordinates function with a successful API call"""

        # Mocking the googlemaps.Client.geocode method
        with patch("googlemaps.Client.geocode") as mock_geocode:
            mock_geocode.return_value = [{
                "geometry": {"location": {"lat": 38.8966, "lng": -104.8049}}
            }]

            result = utils.get_coordinates(
                settings.GOOGLE_MAPS_API_KEY,
                "1420 Austin Bluffs Pkwy, Colorado Springs, CO 80918, USA"
            )

            # Result should be (38.8966, -104.8049)
            self.assertEqual(result, (38.8966, -104.8049))

    def test_get_coordinates_failure(self):
        """Test get_coordinates function when the API call fails"""

        # Mocking the googlemaps.Client.geocode method to simulate failure
        with patch("googlemaps.Client.geocode") as mock_geocode:
            mock_geocode.side_effect = Exception("Google Maps API Error")

            result = utils.get_coordinates(settings.GOOGLE_MAPS_API_KEY, "Test Location")

            # Result should be none
            self.assertIsNone(result)
