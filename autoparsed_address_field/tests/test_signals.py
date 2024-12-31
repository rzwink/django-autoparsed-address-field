import logging
from django.test import TestCase
from autoparsed_address_field.models import Address
from autoparsed_address_field.signals import address_parsed

logger = logging.getLogger(__name__)


# Signal handler defined outside the test class
def signal_receiver(sender, model_name, address_instance, **kwargs):
    """
    Signal receiver to capture and log signal details for tests.
    """
    signal_receiver.signal_received = True
    signal_receiver.received_model_name = model_name
    signal_receiver.received_address_instance = address_instance
    logger.debug("Signal received!")


# Initialize attributes for tracking signal state
signal_receiver.signal_received = False
signal_receiver.received_model_name = None
signal_receiver.received_address_instance = None

# Connect the signal once
address_parsed.connect(signal_receiver, dispatch_uid="test_signal_receiver")


class AddressSignalTest(TestCase):
    def setUp(self):
        # Reset the signal handler state before each test
        signal_receiver.signal_received = False
        signal_receiver.received_model_name = None
        signal_receiver.received_address_instance = None

    def test_signal_on_arcgis_parse(self):
        # Ensure ArcGIS is set as the geocoder provider
        with self.settings(ADDRESS_GEOCODER_PROVIDER="arcgis"):
            raw_address = "123 Mock St, Mock City, MO 43212"
            address = Address.objects.create(raw=raw_address)

            # Assertions
            self.assertTrue(
                signal_receiver.signal_received, "Signal not received for ArcGIS parse."
            )
            self.assertEqual(signal_receiver.received_model_name, "address")
            self.assertEqual(signal_receiver.received_address_instance, address)
            self.assertIsNone(address.formatted)
            self.assertEqual(address.raw, raw_address)

    def test_signal_on_scourgify_parse(self):
        # Ensure Scourgify is set as the geocoder provider
        with self.settings(ADDRESS_GEOCODER_PROVIDER="scourgify"):
            raw_address = "456 Mock Blvd, Mock Town, MT 43212"
            address = Address.objects.create(raw=raw_address)

            # Assertions
            self.assertTrue(
                signal_receiver.signal_received,
                "Signal not received for Scourgify parse.",
            )
            self.assertEqual(signal_receiver.received_model_name, "address")
            self.assertEqual(signal_receiver.received_address_instance, address)
            self.assertIsNotNone(address.formatted)
            self.assertIn("456 MOCK BLVD", address.formatted.upper())
