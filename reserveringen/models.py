from django.db import models
from django.conf import settings
from films.models import Film, Location, Room
from django.utils.timezone import now



class Reservering(models.Model):
    gebruiker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reserveringen'
    )
    event = models.ForeignKey(
        'event',
        on_delete=models.CASCADE,
        related_name='reserveringen',
    )
    aantal_tickets = models.PositiveIntegerField()
    reserveringsdatum = models.DateTimeField(auto_now_add=True)  # Automatisch ingevuld met de datum van reservering
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'In behandeling'),
            ('confirmed', 'Bevestigd'),
            ('cancelled', 'Geannuleerd')
        ],
        default='pending'
    )  # Status van de reservering

    def __str__(self):
        # Filminformatie wordt via event opgehaald
        return f"Reservering door {self.gebruiker.email} voor {self.event.film.title} ({self.aantal_tickets} tickets)"

class Event(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="events")
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # Verwijs naar de juiste app
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Verwijs naar de juiste app
    date = models.DateTimeField()  # Datum en tijd van het event
    totaal_aantal_plekken = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.film.title} - {self.location.name} - {self.date}"
