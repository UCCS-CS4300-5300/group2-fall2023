### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Models

from django.db import models
from django.urls import reverse

# TENTATIVE MODEL CONTENTS
# ID
# Name
# Location
# Date
# Start Time
# End Time

class Event(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])