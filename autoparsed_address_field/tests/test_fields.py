from django.test import TestCase
from autoparsed_address_field.models import Address


class AutoParsedAddressFieldTest(TestCase):
    """
    Test suite for the AutoParsedAddressField with a mock geocoder.
    """

    def setUp(self):
        """
        Set up the test case with a raw address.
        """
        self.address = Address.objects.create(raw="123 Mock St, Mock City, MO")

    def test_address_parsing(self):
        """
        Test that the address is parsed correctly and formatted as expected.
        """
        # Assuming the parsing logic sets the formatted value
        expected_output = "123 MOCK ST, MOCK CITY, MO"
        self.assertEqual(str(self.address), expected_output)
