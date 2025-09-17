import uuid

from django.db import models


class TimeStampedUUIDModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    model_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )


class FilmWork(TimeStampedUUIDModel):
    class Meta:
        db_table = "film_work"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    film_type = models.CharField(max_length=50)
    creation_date = models.DateField(blank=True, null=True)

    genres = models.ManyToManyField("Genre", through="GenreFilmWork")
    persons = models.ManyToManyField("Person", through="PersonFilmWork")


class Genre(TimeStampedUUIDModel):
    class Meta:
        db_table = "genre"

    name = models.CharField(max_length=255)
    description_text = models.TextField(blank=True, null=True)


class Person(TimeStampedUUIDModel):
    class Meta:
        db_table = "person"

    full_name_person = models.CharField(max_length=255)


class GenreFilmWork(models.Model):
    class Meta:
        db_table = "genre_film_work"
        unique_together = ("film_work", "genre")

    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class PersonFilmWork(models.Model):
    class Meta:
        db_table = "person_film_work"
        unique_together = ("film_work", "person", "role")

    role = models.CharField(max_length=50)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
