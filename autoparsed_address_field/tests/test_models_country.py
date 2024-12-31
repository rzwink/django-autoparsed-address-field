from django.test import TestCase
from ..models import Country


class CountryModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the Country model.
        """
        self.country = Country.objects.create(name="United States", code="USA")

    def test_country_creation(self):
        """
        Test that a Country instance can be successfully created.
        """
        self.assertEqual(self.country.name, "United States")
        self.assertEqual(self.country.code, "USA")

    def test_str_representation(self):
        """
        Test the string representation of a Country instance.
        """
        self.assertEqual(str(self.country), "United States")

    def test_unique_name_constraint(self):
        """
        Test that the name field is unique.
        """
        with self.assertRaises(Exception):
            Country.objects.create(name="United States", code="CAN")

    def test_unique_code_constraint(self):
        """
        Test that the code field is unique.
        """
        with self.assertRaises(Exception):
            Country.objects.create(name="Canada", code="USA")

    def test_verbose_name_plural(self):
        """
        Test the verbose_name_plural of the Country model.
        """
        self.assertEqual(Country._meta.verbose_name_plural, "Countries")
