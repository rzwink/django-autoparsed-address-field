from django.test import TestCase
from ..models import Locality, State, Country


class LocalityModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the Locality model.
        """
        # Create a Country and State to associate with Locality
        self.country = Country.objects.create(name="United States", code="USA")
        self.state = State.objects.create(
            name="California", code="CA", country=self.country
        )

        # Create a Locality instance
        self.locality = Locality.objects.create(
            name="Los Angeles", postal_code="90001", state=self.state
        )

    def test_locality_creation(self):
        """
        Test that a Locality instance can be successfully created.
        """
        self.assertEqual(self.locality.name, "Los Angeles")
        self.assertEqual(self.locality.postal_code, "90001")
        self.assertEqual(self.locality.state, self.state)

    def test_str_representation(self):
        """
        Test the string representation of a Locality instance.
        """
        self.assertEqual(str(self.locality), "Los Angeles, California (CA)")

    def test_unique_together_constraint(self):
        """
        Test the unique_together constraint for name, postal_code, and state.
        """
        with self.assertRaises(Exception):
            Locality.objects.create(
                name="Los Angeles", postal_code="90001", state=self.state
            )

    def test_verbose_name_plural(self):
        """
        Test the verbose_name_plural of the Locality model.
        """
        self.assertEqual(Locality._meta.verbose_name_plural, "Localities")
