import logging

from scourgify import normalize_address_record
from scourgify.exceptions import UnParseableAddressError
from uszipcode import SearchEngine
from ..models import Country, State, Locality

logger = logging.getLogger(__name__)


class ScourgifyGeocodingService:
    def parse(self, address_instance):
        try:
            parsed = normalize_address_record(address_instance.raw)
            print(parsed)
        except UnParseableAddressError as e:
            logger.error(
                f"Scourgify could not parse the address: {address_instance.raw} {e}"
            )
            return

        address_instance.address_line_1 = parsed.get("address_line_1", "")
        address_instance.address_line_2 = parsed.get("address_line_2", "")
        locality_name = parsed.get("city", "")
        postal_code = parsed.get("postal_code", "")
        state_name = parsed.get("state", "")

        address_instance.formatted = (
            f"{address_instance.address_line_1 or ''}"
            f"{', ' + address_instance.address_line_2 if address_instance.address_line_2 else ''}, "
            f"{locality_name or ''}, {state_name or ''} {postal_code or ''}".strip(", ")
        )

        country, _ = Country.objects.get_or_create(name="USA")
        state, _ = State.objects.get_or_create(name=state_name, country=country)
        address_instance.locality, _ = Locality.objects.get_or_create(
            name=locality_name, postal_code=postal_code, state=state
        )

        if postal_code:
            search = SearchEngine()
            zipcode = search.by_zipcode(postal_code)
            if zipcode:
                address_instance.latitude = zipcode.lat
                address_instance.longitude = zipcode.lng
