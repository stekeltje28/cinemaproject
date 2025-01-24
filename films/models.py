from django.db import models
from django.utils.timezone import now


# Location Model
from django.db import models

class Location(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitely define the id, although this is optional
    name = models.CharField(max_length=100)  # Naam van de locatie (bijv. Amsterdam, Rotterdam)
    address = models.CharField(max_length=255, null=True, blank=True)  # Optioneel adres
    city = models.CharField(max_length=100, null=True, blank=True)  # Optioneel stad of regio

    def __str__(self):
        return self.name

# Room Model
class Room(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitely define the id, although this is optional
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="rooms")  # Verwijst naar de locatie
    name = models.CharField(max_length=100)  # Naam van de zaal (bijv. Zaal 1, Zaal 2)
    capacity = models.IntegerField()  # Capaciteit van de zaal (aantal stoelen)

    def __str__(self):
        return f"{self.name} - {self.location.name}"

# Film Model
from django.db import models

# Film Model
class Film(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateTimeField(default=now)
    afbeelding = models.ImageField(upload_to='films/', null=True, blank=True)
    beschrijving = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=100)
    min_leeftijd = models.IntegerField()
    rooms = models.ManyToManyField(Room, related_name="films", blank=True)  # Dit zou moeten werken

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Films"

    def __str__(self):
        return self.title


