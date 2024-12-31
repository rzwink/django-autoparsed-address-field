from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from autoparsed_address_field.admin import (
    CountryAdmin,
    StateAdmin,
    LocalityAdmin,
    AddressAdmin,
)
from autoparsed_address_field.models import Country, State, Locality, Address


class MockRequest:
    pass


class CountryAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = CountryAdmin(Country, self.site)

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ("name", "code"))

    def test_search_fields(self):
        self.assertEqual(self.admin.search_fields, ("name", "code"))

    def test_ordering(self):
        self.assertEqual(self.admin.ordering, ("name",))


class StateAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = StateAdmin(State, self.site)

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ("name", "code", "country"))

    def test_search_fields(self):
        self.assertEqual(self.admin.search_fields, ("name", "code", "country__name"))

    def test_list_filter(self):
        self.assertEqual(self.admin.list_filter, ("country",))

    def test_ordering(self):
        self.assertEqual(self.admin.ordering, ("country", "name"))


class LocalityAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = LocalityAdmin(Locality, self.site)

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ("name", "postal_code", "state"))

    def test_search_fields(self):
        self.assertEqual(
            self.admin.search_fields,
            ("name", "postal_code", "state__name", "state__country__name"),
        )

    def test_list_filter(self):
        self.assertEqual(self.admin.list_filter, ("state", "state__country"))

    def test_ordering(self):
        self.assertEqual(self.admin.ordering, ("state__country", "state", "name"))


class AddressAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = AddressAdmin(Address, self.site)
        self.country = Country.objects.create(name="Test Country", code="TC")
        self.state = State.objects.create(
            name="Test State", code="TS", country=self.country
        )
        self.locality = Locality.objects.create(
            name="Test Locality", postal_code="12345", state=self.state
        )
        self.address = Address.objects.create(
            raw="123 Test St, Test Locality, TS",
            formatted="123 Test St, Test Locality, TS",
            address_line_1="123 Test St",
            locality=self.locality,
            latitude=40.7128,
            longitude=-74.0060,
        )

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            (
                "id",
                "raw",
                "formatted",
                "address_line_1",
                "locality",
                "latitude",
                "longitude",
            ),
        )

    def test_search_fields(self):
        self.assertEqual(
            self.admin.search_fields,
            (
                "formatted",
                "address_line_1",
                "locality__name",
                "locality__state__name",
                "locality__state__country__name",
            ),
        )

    def test_list_filter(self):
        self.assertEqual(self.admin.list_filter, ("locality__state__country",))

    def test_ordering(self):
        self.assertEqual(
            self.admin.ordering,
            ("locality__state__country", "locality__state", "locality", "formatted"),
        )
