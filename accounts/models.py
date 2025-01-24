from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None, **extra_fields):
        if not email:
            raise ValueError('Het e-mailadres moet worden opgegeven.')
        if not name:
            raise ValueError('De naam moet worden opgegeven.')  # Hier ontstaat de fout
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser moet is_staff=True hebben.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser moet is_superuser=True hebben.')

        return self.create_user(email, password, name=name, **extra_fields)



# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    leeftijd = models.CharField(max_length=3)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# User Data Model
class UserData(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='userdata'
    )  # Koppeling met de gebruiker

    naam = models.CharField(max_length=50)
    profiel_foto = models.ImageField(default='default_profile.webp')
    reserveringen = models.JSONField(default=list, blank=True)  # Recente boekingen van films
    opgeslagen = models.JSONField(default=list, blank=True)  # Film evenementen
    leeftijd = models.PositiveIntegerField(null=True, blank=True)
    aantal_recente_reserveringen = models.PositiveIntegerField(default=0)  # Aantal recente reserveringen van films
    taal = models.CharField(max_length=50, default='Nederlands')  # Voorkeur films
    favoriete_genres = models.JSONField(default=list, blank=True)  # Lijst van favoriete genres (bijv. ['Actie', 'Drama'])

    def __str__(self):
        return f"UserData voor {self.user.email}"

    class Meta:
        verbose_name = 'User Data'
        verbose_name_plural = 'User Data'
