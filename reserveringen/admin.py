from django.contrib import admin
from .models import Reservering, Event

@admin.register(Reservering)
class ReserveringAdmin(admin.ModelAdmin):
    list_display = ('gebruiker', 'aantal_tickets', 'status', 'reserveringsdatum', 'event')
    list_filter = ('status', 'reserveringsdatum')
    search_fields = ('gebruiker__email', 'film__title')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('film', 'location', 'room', 'date', 'totaal_aantal_plekken')  # Welke velden zichtbaar zijn in de lijst
    list_filter = ('film', 'location', 'room')  # Filters om snel te filteren in de lijst
    search_fields = ('film__title', 'location__name', 'room__name')  # Doorzoekbare velden in de admin
    date_hierarchy = 'date'  # Maakt een datum hiërarchie mogelijk voor de datumfilter

