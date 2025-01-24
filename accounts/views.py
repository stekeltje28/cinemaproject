from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import json
from .models import CustomUser, UserData
from films.models import Film, Location
from films.models import Location, Room
from reserveringen.models import Event


# Registratie van een gebruiker
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        name = data.get('name')
        leeftijd = data.get('leeftijd')

        # Controleer of de wachtwoorden overeenkomen
        if password1 != password2:
            return JsonResponse({'error': 'Wachtwoorden komen niet overeen'}, status=400)

        # Controleer of de e-mail al geregistreerd is
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Er bestaat al een gebruiker met dit e-mailadres.")
            return redirect("register")

        # Probeer de gebruiker aan te maken en in te loggen
        try:
            user = CustomUser.objects.create_user(email=email, password=password1, name=name, leeftijd=leeftijd)
            login(request, user)  # Log de gebruiker automatisch in
            return JsonResponse({'success': True})  # Geef succes terug bij succesvolle registratie
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)  # Retourneer fout als registratie mislukt
    else:
        return JsonResponse({'error': 'POST vereist'}, status=405)  # Alleen POST-requests toegestaan


# Inloggen van een gebruiker
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json

def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON-data verwerken
            username = data.get('email')  # Ophalen van email
            password = data.get('password')  # Ophalen van wachtwoord

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Inloggen succesvol!', 'is_logged_in': True})
            else:
                return JsonResponse({'message': 'Ongeldige inloggegevens.', 'is_logged_in': False})

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Ongeldig JSON-formaat.', 'is_logged_in': False})

    return JsonResponse({'message': 'Alleen POST-verzoeken worden ondersteund.', 'is_logged_in': False})

def user_logout(request):
    logout(request)
    return JsonResponse({'success': True})

# Controle of gebruiker ingelogd is
def check_logged_in(request):
    return JsonResponse({'is_logged_in': request.user.is_authenticated})


from django.shortcuts import render, redirect
from .models import UserData

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_data = UserData.objects.filter(user=request.user).first()
    if not user_data:
        user_data = UserData.objects.create(user=request.user, naam=request.user.name or "Onbekend")

    if request.user.is_superuser:
        locations = Location.objects.all()
        rooms = Room.objects.all()
        films = Film.objects.all()
        events = Event.objects.all()
        return render(request, 'medewerkers_dashboard.html', {
            'locations': locations, 'rooms': rooms,
            'films': films, 'user_data': user_data,
            'events': events
        })
    else:
        return render(request, 'user_dashboard.html', {
            'user_data': user_data,

        })
