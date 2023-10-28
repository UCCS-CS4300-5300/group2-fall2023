### CS 4300 Fall 2023 Group 2
### Harvestly
### Events Models

from django.db import models

# TENTATIVE MODEL CONTENTS
# ID
# Name
# Location
# Date
# Start Time
# End Time
# Farmers <- From Farmer model
# Products <- Probably from other model?
# Customers <- From Customer model

class Event(models.Model):
    event_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)
    # temporary hard-coded product-list for sprint 1
    product_list = (

    )
    
    # class Farmers(models.Model):

    # class Products(models.Model):

    # class Customers(models.Model):