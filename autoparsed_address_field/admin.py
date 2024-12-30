from django.contrib import admin
from .models import Country, State, Locality, Address


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
    ordering = ("name",)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "country")
    search_fields = ("name", "code", "country__name")
    list_filter = ("country",)
    ordering = ("country", "name")


@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    list_display = ("name", "postal_code", "state")
    search_fields = ("name", "postal_code", "state__name", "state__country__name")
    list_filter = ("state", "state__country")
    ordering = ("state__country", "state", "name")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "raw",
        "formatted",
        "address_line_1",
        "locality",
        "latitude",
        "longitude",
    )
    search_fields = (
        "formatted",
        "address_line_1",
        "locality__name",
        "locality__state__name",
        "locality__state__country__name",
    )
    list_filter = ("locality__state__country",)
    ordering = ("locality__state__country", "locality__state", "locality", "formatted")
