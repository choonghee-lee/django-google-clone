from django.db import models


class Site(models.Model):
    """
    파싱한 웹 사이트의 정보를 나타내는 모델

    url:            웹사이트 URL
    title:          <title>타이틀</title>
    description:    <meta>
    keywords:       <meta>
    clicks:         클릭된 수
    """
    url = models.URLField()
    title = models.CharField(max_length=512)
    description = models.CharField(max_length=512, blank=True)
    keywords = models.CharField(max_length=512, blank=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.title + " - " + self.url


class Image(models.Model):
    """
    파싱한 이미지의 정보를 나타내는 모델

    site_url:   웹사이트 URL
    image_url:  이미지 URL
    title:      <img title="">
    alt:        <img alt="">
    clicks:     클릭된 수
    broken:     링크가 깨졌는지?
    """
    site_url = models.URLField()
    image_url = models.URLField()
    title = models.CharField(max_length=512, blank=True)
    alt = models.CharField(max_length=512, blank=True)
    clicks = models.IntegerField(default=0)
    broken = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " - " + self.image_url
