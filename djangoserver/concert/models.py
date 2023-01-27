from django.db import models
from django.conf import settings
from django.utils.timezone import now


# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=200, null=False)
    artist_name = models.CharField(max_length=100)
    length = models.IntegerField()
    pub_date = models.DateTimeField('publish date')
    image_url = models.CharField(max_length=256, null=True)
    genres = models.CharField(max_length=200, null=True)
    lyrics = models.CharField(max_length=1000)


class Concert(models.Model):
    title = models.CharField(max_length=200, null=False)
    songs = models.ManyToManyField(Song)
    poster = models.ImageField(upload_to='poster_images/')
    artist_name = models.CharField(max_length=100)
    total_registrations = models.IntegerField(default=0)
    release_date = models.DateTimeField('release date')
    is_registrated = False


class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    date_registrated = models.DateField(default=now)
