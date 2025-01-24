from django import forms
from .models import Location, Room, Film

# Formulier voor het toevoegen van een locatie
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'city']  # Geen 'id'

# Formulier voor het toevoegen van een zaal
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'location']  # Geen 'id'

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['title', 'afbeelding', 'beschrijving', 'genre', 'min_leeftijd' ]