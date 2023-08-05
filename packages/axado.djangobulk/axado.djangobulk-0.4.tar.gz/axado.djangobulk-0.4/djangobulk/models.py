from django.db import models


class TestModelA(models.Model):
    a = models.CharField(max_length=200)
    b = models.IntegerField()
    c = models.IntegerField()


class TestModelDate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
