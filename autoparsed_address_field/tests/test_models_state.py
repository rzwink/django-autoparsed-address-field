from django.test import TestCase
from ..models import Country


class CountryModelTest(TestCase):
    def setUp(self):
        """
        Create a sample country for testing.
        """
        self.country = Country.objects.create(name="United States", code="USA")

    def test_country_creation(self):
        """
        Test that a country can be successfully created.
        """
        self.assertEqual(self.country.name, "United States")
        self.assertEqual(self.country.code, "USA")

    def test_country_str_method(self):
        """
        Test the `__str__` method of the Country model.
        """
        self.assertEqual(str(self.country), "United States")

    def test_unique_name_constraint(self):
        """
        Test that the `name` field is unique.
        """
        with self.assertRaises(Exception):
            Country.objects.create(name="United States", code="CAN")

    def test_unique_code_constraint(self):
        """
        Test that the `code` field is unique.
        """
        with self.assertRaises(Exception):
            Country.objects.create(name="Canada", code="USA")
