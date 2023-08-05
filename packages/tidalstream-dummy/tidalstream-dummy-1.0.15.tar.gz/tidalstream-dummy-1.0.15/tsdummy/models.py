from django.db import models


class DatabaseStuff(models.Model):
    stuff = models.CharField(max_length=10)
