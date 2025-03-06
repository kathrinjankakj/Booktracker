from django.contrib.auth.models import User
from django.db import models
import datetime
from django.core.exceptions import ValidationError


# Create your models here.
class Book(models.Model):

    LANGUAGE_OPTIONS = {"Englisch":"English", "Deutsch":"Deutsch", "Französisch":"Français", "Spanisch":"Español", "Italienisch":"Italiano"}
    KATEGORIEN = {"Romanze":"Romanze", "Historischer Roman":"Historischer Roman", "Krimi":"Krimi", "Thriller":"Thriller", "Fantasy":"Fantasy", "Science Fiction":"Science Fiction", "Sachbuch":"Sachbuch",
                  "Biografie":"Biografie", "Sonstige":"Sonstige"}

    def validate_publication_date(value):
        allowed_years=datetime.date.today().year+10
        if value and (value < 1000 or value > allowed_years):
            raise ValidationError('Erscheinungsdatum muss zwischen 1000 und '+ str(allowed_years) +' liegen.')


    titel = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    buchcover = models.ImageField(blank=True, null=True, db_default='default.png')
    seitenanzahl = models.IntegerField(blank=True, null=True)
    beschreibung = models.TextField(blank=True, null=True, default='Geben Sie eine kurze Beschreibung über den Inhalt des Buches an.')
    erscheinungsdatum = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[validate_publication_date]
    )
    sprache = models.CharField(blank=True, null=True, max_length=50, choices=LANGUAGE_OPTIONS)

    kategorie = models.CharField(blank=True, null=True, max_length=50, choices=KATEGORIEN)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.titel} ({self.id})'


class UserGallery(models.Model):
    TRACKING_OPTIONS = {"None": "None","Geplant":"Geplant", "Begonnen":"Begonnen", "Gelesen":"Gelesen"}
    # RATING_OPTIONS = {"Charakterentwicklung":"Charakterentwicklung", "Spannung":"Spannung",
    #                   "Themenvielfalt":"Themenvielfalt", "Schreibstil":"Schreibstil", "Botschaft":"Botschaft", "Alles": "Alles"}
    # RATINGS = {"0": "Nicht bewertet", "1": "Ein Stern", "2": "Zwei Sterne", "3": "Drei Sterne", "4": "Vier Sterne",
    #            "5": "Fünf Sterne"}

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    tracker = models.CharField(blank=True, null=True, max_length=50, choices=TRACKING_OPTIONS,
                               help_text='Geben Sie Ihren Lesestatus zum Buch an.')
    #Startdatum
    begonnen = models.DateField(blank=True, null=True, help_text="Startdatum des Lesens.")
    #Aktuelle Seite
    fortschritt = models.IntegerField(blank=True, null=True, help_text="Aktuelle Seite.")
    bewertung = models.CharField(blank=True, null=True, max_length=50)
    inhaltsfokus = models.CharField(blank=True, null=True, max_length=50, help_text='Was hat Ihnen inhaltlich am besten gefallen?')

    def __str__(self):
        return f"{self.user.username} - {self.book.titel} ({self.tracker})"
