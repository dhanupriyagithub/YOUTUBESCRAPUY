from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=100)

class Video(models.Model):
    title = models.CharField(max_length=200)
    views = models.PositiveIntegerField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
