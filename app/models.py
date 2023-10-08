from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Query(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    query_text = models.TextField()




