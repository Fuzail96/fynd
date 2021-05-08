from django.db import models


class Genre(models.Model):
    """
    Genre model : model for movie Genres
    """
    name = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    Movie model : model for Movies
    """
    name = models.CharField(max_length=500)
    director = models.CharField(max_length=500)
    genre = models.ManyToManyField(Genre)
    popularity = models.FloatField()
    imdb_score = models.FloatField()

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.name
