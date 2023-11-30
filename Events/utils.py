### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Utilities

""" Implmentation of Google Maps API utilities """

import googlemaps

def get_coordinates(api_key, address):
    """ Given an address string and an the API KEY convert address to coordinates. 
    
    returns (latitude, longiutde) | None
    """

    gm = googlemaps.Client(api_key)

    try:
        geo = gm.geocode(address)

        if geo:
            coordinates = geo[0]["geometry"]["location"]

            latitude = coordinates["lat"]
            longitude = coordinates["lng"]

            return (latitude, longitude)

        return None

    except Exception as e:
        return None
