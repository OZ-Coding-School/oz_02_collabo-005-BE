from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from taggit.managers import TaggableManager

class Restaurant(models.Model):

    STATUS_CHOICES = (
        (1, 'Open'),
        (2, 'Closed'),
        (3, 'Under Maintenance'),
    )

    name = models.CharField(max_length=50)
    representative_menu = models.PositiveIntegerField()

    @property
    def representative_menu_picture_url(self):
        if self.representative_menu_picture:
            return self.representative_menu_picture.url
        else:
            return None
        
    description = models.TextField()
    notice = models.TextField()
    delivery_fee = models.PositiveIntegerField()
    minimum_order_amount = models.PositiveIntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    status = models.PositiveIntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return f'({self.id}){self.name}'

"""Hasgtag model"""
class Hashtag(models.Model):
    hashtag = models.CharField(max_length=20)

    def __str__(self):
        return self.hashtag

class RestaurantHashtag(models.Model):
    """hashtags는 역참조를 하기 위한 역할"""
    restaurant = models.ForeignKey(Restaurant, related_name='hashtags', on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.restaurant} - {self.hashtag}'

"""Category model"""
class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category

class RestaurantCategory(models.Model):
    """categories는 역참조를 하기 위한 역할"""
    restaurant = models.ForeignKey(Restaurant, related_name='categories', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.restaurant} - {self.category}'

