from django.db import models


class Site(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=512)
    description = models.CharField(max_length=512, blank=True)
    keywords = models.CharField(max_length=512, blank=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.title + " - " + self.url


class Image(models.Model):
    site_url = models.URLField()
    image_url = models.URLField()
    title = models.CharField(max_length=512, blank=True)
    alt = models.CharField(max_length=512, blank=True)
    clicks = models.IntegerField(default=0)
    broken = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " - " + self.image_url
