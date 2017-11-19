from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=128)
    contributors = models.ManyToManyField(to='Contributor', related_name='movies')

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=128)

    @property
    def related_movies(self):
        return Movie.objects.filter(contributors__genre=self).distinct()

    def __str__(self):
        return self.name


class Contributor(models.Model):
    name = models.CharField(max_length=128)
    genre = models.ForeignKey(to=Genre, related_name='contributors')

    def __str__(self):
        return self.name
