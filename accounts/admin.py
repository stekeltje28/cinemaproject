from django.contrib import admin
from .models import CustomUser, UserData
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    # Velden die worden weergegeven in de lijstweergave van de admin
    list_display = ('email', 'name', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'name')

    # Velden voor detailweergave en bewerkpagina
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Persoonlijke informatie', {'fields': ('name',)}),
        ('Permissies', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Belangrijke data', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )

# Register het CustomUser-model met de aangepaste admin-configuratie
admin.site.register(CustomUser, CustomUserAdmin)

class UserDataAdmin(admin.ModelAdmin):
    # Velden die worden weergegeven in de lijstweergave van de admin
    list_display = ('user', 'naam', 'leeftijd', 'aantal_recente_reserveringen', 'taal', 'profiel_foto')
    search_fields = ('naam', 'user__email')
    list_filter = ('taal',)
    ordering = ('user__email',)

    # Detailweergave in de admin
    fieldsets = (
        (None, {'fields': ('user', 'naam', 'leeftijd', 'taal', 'profiel_foto')}),
        ('Reserveringen', {'fields': ('reserveringen', 'aantal_recente_reserveringen')}),
        ('Voorkeuren', {'fields': ('opgeslagen', 'favoriete_genres')}),
    )

# Register het UserData-model met de aangepaste admin-configuratie
admin.site.register(UserData, UserDataAdmin)
