from autoparsed_address_field.models import Address, Locality, State, Country


def create_address_from_keys(address_data, skip_parsing=False):
    """
    Creates and saves an Address instance directly from a dictionary
    where keys match the Address model structure.

    Args:
        address_data (dict): A dictionary containing address fields.
        skip_parsing (bool): Whether to skip parsing the address fields.

    Returns:
        Address: The created Address instance.
    """
    # Fetch or create the country
    country, _ = Country.objects.get_or_create(
        name=address_data.get("country_name"),
        code=address_data.get("country_code"),
    )

    # Fetch or create the state
    state, _ = State.objects.get_or_create(
        name=address_data.get("state_name"),
        country=country,
    )

    # Fetch or create the locality
    locality, _ = Locality.objects.get_or_create(
        name=address_data.get("locality_name"),
        postal_code=address_data.get("postal_code"),
        state=state,
    )

    # Create the Address instance without saving
    address = Address(
        address_line_1=address_data.get("address_line_1"),
        address_line_2=address_data.get("address_line_2"),
        locality=locality,
        raw=", ".join(
            filter(
                None,
                [
                    address_data.get("address_line_1"),
                    address_data.get("address_line_2"),
                    address_data.get("locality_name"),
                    address_data.get("state_name"),
                    address_data.get("postal_code"),
                    address_data.get("country_name"),
                ],
            )
        ),
        formatted=f"{address_data.get('address_line_1')}, {address_data.get('locality_name')}, "
        f"{address_data.get('state_name')} {address_data.get('postal_code')}".strip(),
        latitude=address_data.get("latitude"),
        longitude=address_data.get("longitude"),
    )

    # Save with skip_parsing=True
    address.save(skip_parsing=skip_parsing)

    return address
