from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from films import views as films_views
from reserveringen import views as reservering_views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('check-logged-in/', views.check_logged_in, name='check_logged_in'),
    path('dashboard/', views.dashboard, name='dashboard'),


    path('locations/', films_views.location_list, name='location_list'),
    path('locations/add/', films_views.add_location, name='add_location'),
    path('locations/add-room/', films_views.add_room, name='add_room'),
    path('films/add/', films_views.add_film, name='add_film'),
    path('films/<int:film_id>/', films_views.film_detail, name='film_detail'),
    path('location/<int:location_id>/delete/', films_views.delete_location, name='delete_location'),
    path('room/<int:room_id>/delete/', films_views.delete_room, name='delete_room'),

    path('assign/', reservering_views.assign_film_date_location, name='assign_film_date_location'),
    path('events/edit/<int:event_id>/', reservering_views.edit_event, name='edit_event'),
]
