from django.db import models


class Exercise(models.Model):
    image_url = "https://img.youtube.com/vi/{}/hqdefault.jpg"
    name = models.CharField("Name", max_length=256)
    description = models.TextField("Description")
    link = models.URLField("URL")
