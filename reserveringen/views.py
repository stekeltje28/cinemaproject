from django.shortcuts import render, redirect
from .models import Reservering
from .forms import ReserveringForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from reserveringen.models import Event

@login_required
def reservering(request, film_id):
    if request.method == 'POST':
        event_id = request.POST['event']
        aantal_tickets = int(request.POST['aantal'])
        event = get_object_or_404(Event, id=event_id)

        if event.totaal_aantal_plekken >= aantal_tickets:
            event.totaal_aantal_plekken -= aantal_tickets
            event.save()
            messages.success(request, 'Reservering succesvol!')
        else:
            messages.error(request, 'Niet genoeg plekken beschikbaar.')

        return redirect('film_detail', film_id=film_id)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Film, Location, Room, Event
from django.http import HttpResponseBadRequest

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Film, Location, Room, Event
from datetime import datetime
from django.utils.timezone import make_aware

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime
from django.core.exceptions import ValidationError
from films.models import Film, Location, Room

def assign_film_date_location(request):
    if request.method == "POST":
        film_id = request.POST.get('film')
        location_id = request.POST.get('location')
        room_id = request.POST.get('zaal')
        datum_list = request.POST.getlist('datum[]')
        tijd_list = request.POST.getlist('tijd[]')
        beschikbare_plaatsen_id = request.POST.get('beschikbare_plaatsen')

        # Validate fields
        if not film_id or not location_id or not room_id or not datum_list or not tijd_list:
            messages.error(request, "Alle velden zijn verplicht.")
            return redirect('dashboard')

        try:
            beschikbare_plaatsen = int(beschikbare_plaatsen_id)
        except ValueError:
            messages.error(request, "Aantal beschikbare plaatsen moet een geldig getal zijn.")
            return redirect('dashboard')

        # Get objects
        film = get_object_or_404(Film, id=film_id)
        location = get_object_or_404(Location, id=location_id)
        room = get_object_or_404(Room, id=room_id)

        if room.location != location:
            messages.error(request, "De geselecteerde zaal hoort niet bij de geselecteerde locatie.")
            return redirect('dashboard')

        # Create events
        success_count = 0
        failure_count = 0
        for datum, tijd in zip(datum_list, tijd_list):
            try:
                combined_datetime = datetime.strptime(f"{datum} {tijd}", "%Y-%m-%d %H:%M")
                combined_datetime = make_aware(combined_datetime)

                Event.objects.create(
                    film=film,
                    location=location,
                    room=room,
                    date=combined_datetime,
                    totaal_aantal_plekken=beschikbare_plaatsen
                )
                success_count += 1
            except Exception as e:
                failure_count += 1
                messages.error(request, f"Fout bij {datum} {tijd}: {str(e)}")

        # Show results
        if success_count > 0:
            messages.success(request, f"{success_count} evenementen succesvol aangemaakt.")
        if failure_count > 0:
            messages.error(request, f"{failure_count} evenementen konden niet worden aangemaakt.")
        return redirect('dashboard')

    # GET: Render form
    films = Film.objects.all()
    locations = Location.objects.all()
    rooms = Room.objects.all()
    return render(request, 'assign_film_date_location.html', {
        'films': films,
        'locations': locations,
        'rooms': rooms
    })


def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EventForm(instance=event)

    return render('dashboard')
