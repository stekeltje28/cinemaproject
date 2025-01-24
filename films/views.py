# accounts/views.py
from django.shortcuts import render, get_object_or_404
from .models import Location, Room, Film
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from films.forms import FilmForm
from .forms import FilmForm, LocationForm
from films.models import Location, Room
from reserveringen.models import Event



# View voor het weergeven van alle locaties
def location_list(request):
    locations = Location.objects.all()  # Alle locaties ophalen
    messages.success(request, 'Het is gelukt!')
    return redirect('/accounts/dashboard')


def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)  # Maak een formulier op basis van de POST-data
        if form.is_valid():
            form.save()  # Sla de nieuwe locatie op
            return redirect('/accounts/dashboard')
    else:
        form = LocationForm()  # Maak een leeg formulier voor een nieuwe locatie
    return redirect('/accounts/dashboard')

# View voor het toevoegen van een nieuwe zaal
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import RoomForm
from .models import Location


def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room succesvol toegevoegd!')
            return redirect('dashboard')  # Of een andere URL
    else:
        form = RoomForm()

    # Ophalen van de locaties om ze weer te geven in de template
    locations = Location.objects.all()

    return redirect('dashboard')
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # Verwijder de zaal
    room.delete()

    messages.success(request, 'het is gelukt!')

    return redirect('/accounts/dashboard')


from django.shortcuts import get_object_or_404, redirect
from .models import Location


def delete_location(request, location_id):
    # Zoek de locatie op basis van de ID
    location = get_object_or_404(Location, id=location_id)

    # Verwijder de locatie
    location.delete()

    messages.success(request, 'het is gelukt!')


    return redirect('/accounts/dashboard')

from django.shortcuts import render, redirect

def add_film(request):
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES)  # Formuliergegevens en bestanden verwerken
        if form.is_valid():
            form.save()  # Film opslaan in de database
            messages.success(request, 'Film succesvol toegevoegd!')
            return redirect('/accounts/dashboard')  # Redirect naar het dashboard na succesvolle toevoeging
        else:
            messages.error(request, 'Er is iets mis gegaan bij het toevoegen van de film!')
            return redirect('/accounts/films/add/')  # Redirect terug naar de film toevoeg-pagina bij fout
    else:
        # Als het geen POST-aanroep is, direct doorsturen naar dashboard
        return redirect('/accounts/dashboard')  # Direct naar het dashboard


# View voor het tonen van filmdetails
def film_detail(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    events = Event.objects.filter(film=film)

    context = {
        'film': film,
        'events': events,
    }
    return render(request, 'film_detail.html', context)

def film_list(request):
    films = Film.objects.all()

    # Filters toepassen
    locatie_filter = request.GET.getlist('locatie[]')
    genre_filter = request.GET.get('genre')
    min_leeftijd_filter = request.GET.get('min_leeftijd')
    film_naam_filter = request.GET.get('film_naam')

    # Filteren op locatie
    if locatie_filter:
        films = films.filter(events__location__name__in=locatie_filter)

    # Filteren op genre
    if genre_filter:
        films = films.filter(genre__iexact=genre_filter)

    # Filteren op minimum leeftijd
    if min_leeftijd_filter and min_leeftijd_filter.isdigit():
        films = films.filter(min_leeftijd__gte=int(min_leeftijd_filter))

    # Filteren op film naam
    if film_naam_filter:
        films = films.filter(title__icontains=film_naam_filter)

    context = {
        'films': films,
        'locations': Location.objects.all(),
        'locatie_filter': locatie_filter,  # Doorgeven van geselecteerde locaties
        'genre_filter': genre_filter,
        'film_naam_filter': film_naam_filter,
    }
    return render(request, 'film_list.html', context)
