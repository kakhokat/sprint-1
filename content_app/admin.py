from django.contrib import admin

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    extra = 1
    autocomplete_fields = ["genre"]


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 1
    autocomplete_fields = ["person"]


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ("title", "film_type", "creation_date")
    search_fields = ("title",)
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)
