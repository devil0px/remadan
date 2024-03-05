from django.db import models


# Create your models here.


class Accounts(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Cards(models.Model):
    card_number = models.IntegerField( unique=True)
    card_value = models.FloatField(max_length=100)
    card_still = models.CharField(max_length=100)
    price = models.CharField(max_length=100)

    def __str__(self):
        return self.card_number

    class Meta:
        verbose_name_plural = "Cards"

