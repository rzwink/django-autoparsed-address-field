import hashlib
import uuid

from django.conf import settings


def generate_uuid_from_address(address):
    """
    Generates a consistent UUID based on the provided address and a salt.

    :param address: The address string to base the UUID on.
    :param salt: A salt string to add uniqueness and security (default is "default_salt").
    :return: A UUID4 string.
    """
    if not address:
        raise ValueError("Address cannot be empty.")

    salt = getattr(settings, "ADDRESS_SALT", "default-salt")

    # Combine the address and salt
    unique_string = f"{salt}:{address}".lower()

    # Create a hash of the unique string
    hashed = hashlib.sha256(unique_string.encode("utf-8")).hexdigest()

    # Use the hash to create a UUID
    return str(uuid.UUID(hashed[:32]))
