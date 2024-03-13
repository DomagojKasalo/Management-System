from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Korisnik, Predmeti, Uloge, Upis

# Register your models here.

admin.site.register(Predmeti)
admin.site.register(Uloge)
admin.site.register(Upis)

@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('None', {'fields':('uloge', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('None', {'fields':('uloge', 'status')}),
    )

