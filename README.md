# django-autoparsed-address-field

**django-autoparsed-address-field** provides a set of pre-defined models and utilities to manage, normalize, and geocode address data in Django projects. It also offers a custom `AutoParsedAddressField` that integrates seamlessly into your models and automatically parses raw address strings.

## Features

- **Pre-defined Models**:
  - `Country`, `State`, `Locality`, and `Address` models included.
  - Designed with foreign key relationships to represent geographic data.
- **Automatic Address Parsing**:
  - Parse raw address strings into structured fields.
- **Geocoding Providers**:
  - Supports ArcGIS (via `geopy`) and Scourgify for geocoding and normalization.
- **Custom Address Field**:
  - The `AutoParsedAddressField` can be added to any model to handle address data automatically.
- **Admin Mixin**:
  - Simplifies admin integration, displaying a text input for new records and a dropdown for existing ones.

---

## Installation

Install the package via pip:

```bash
pip install django-autoparsed-address-field
```

---

## Usage

### 1. Add `autoparsed_address_field` to `INSTALLED_APPS`

Add the app to your Django project's `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "autoparsed_address_field",
]
```

### 2. Run Migrations

Apply the migrations to create the provided models:

```bash
python manage.py makemigrations autoparsed_address_field
python manage.py migrate
```

### 3. Use the Pre-defined Models

The following models are included in the app and ready for use:

#### `Country`
Represents a country, with a unique ISO code.

```python
from autoparsed_address_field.models import Country

country = Country.objects.create(name="United States", code="USA")
```

#### `State`
Represents a state or region within a country.

```python
from autoparsed_address_field.models import State

state = State.objects.create(name="California", code="CA", country=country)
```

#### `Locality`
Represents a city or locality within a state.

```python
from autoparsed_address_field.models import Locality

locality = Locality.objects.create(name="Los Angeles", postal_code="90001", state=state)
```

#### `Address`
Represents an address, with optional latitude and longitude.

```python
from autoparsed_address_field.models import Address

address = Address.objects.create(
    address_line_1="123 Main Street",
    address_line_2="Apt 4B",
    locality=locality,
    raw="123 Main Street, Los Angeles, CA 90001, USA",
)
```

---

### 4. Use `AutoParsedAddressField`

The `AutoParsedAddressField` provides seamless integration for address parsing in your own models.

#### Example:

```python
from django.db import models
from autoparsed_address_field.fields import AutoParsedAddressField

class YourModel(models.Model):
    address = AutoParsedAddressField()

# When a new instance is saved, the address will be automatically parsed.
your_instance = YourModel.objects.create(
    address=Address.objects.create(raw="1600 Pennsylvania Ave NW, Washington, DC")
)
print(your_instance.address.formatted)
```

---

### 5. Use `AutoParsedAddressAdminMixin`

The `AutoParsedAddressAdminMixin` simplifies admin integration for models using `AutoParsedAddressField`.

#### Example:

```python
from django.contrib import admin
from autoparsed_address_field.admin_mixins import AutoParsedAddressAdminMixin
from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(AutoParsedAddressAdminMixin, admin.ModelAdmin):
    list_display = ("id", "address")
```
#### Admin Behavior:
- **New Records**: Displays a text input for raw address entry.
- **Existing Records**: Displays a dropdown for selecting related `Address` objects.

---
### 6. Using the `address_parsed` Signal

The `address_parsed` signal allows you to hook into the address parsing process. This can be useful if you want to perform additional actions, such as logging, updating related models, or triggering external services when an address is successfully parsed.

#### Example Usage:

```python
from autoparsed_address_field.signals import address_parsed
import logging

logger = logging.getLogger(__name__)

# Define a signal handler
def handle_address_parsed(sender, model_name, address_instance, **kwargs):
    """
    Signal handler for the `address_parsed` signal.

    Args:
        sender: The class of the sender.
        model_name: The name of the model where the address was parsed.
        address_instance: The instance of the Address model that was parsed.
        **kwargs: Additional keyword arguments.
    """
    logger.info(f"Address parsing completed for model: {model_name}")
    logger.info(f"Formatted Address: {address_instance.formatted}")
    logger.info(f"Latitude: {address_instance.latitude}, Longitude: {address_instance.longitude}")
    # Perform additional actions here, such as notifying a user or updating related data

# Connect the signal to the handler
address_parsed.connect(handle_address_parsed, dispatch_uid="handle_address_parsed_signal")
```

#### Explanation:
1. **Signal Handler**: The `handle_address_parsed` function is invoked whenever the signal is dispatched. It receives the sender, the model name, the parsed address instance, and any additional arguments.
2. **Logging**: The handler logs the parsed address details, including the formatted address, latitude, and longitude.
3. **Connecting the Signal**: The `address_parsed.connect` method connects the handler to the signal. The `dispatch_uid` ensures the handler is not connected multiple times.

This setup allows you to extend the functionality of the package by reacting to successful address parsing events in a modular way.


---

## Settings

### Geocoding Provider

The `ADDRESS_GEOCODER_PROVIDER` setting determines which geocoding provider the package uses to parse and normalize addresses. This flexibility allows you to select the provider that best suits your needs based on data accuracy, cost, or specific features.

Add the following to your `settings.py` file to configure the geocoding provider:

```python
ADDRESS_GEOCODER_PROVIDER = "arcgis"  # Options: "arcgis", "scourgify"
```

#### Rationale for Choosing a Provider

| Provider      | Description                                                                 | Rationale                                                                                     |
|---------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| **ArcGIS**    | Leverages Esri's ArcGIS geocoding service via the `geopy` library.          | Best for applications requiring high accuracy, global coverage, and detailed geospatial data. |
| **Scourgify** | Uses `usaddress-scourgify` for parsing and normalizing US addresses.        | Ideal for US-based projects where simplicity and no external dependencies are preferred.      |

#### Example Configuration:

```python
# settings.py

ADDRESS_GEOCODER_PROVIDER = "arcgis"  # Use Esri's ArcGIS geocoder
```

#### Switching Between Providers

You can easily switch between providers by updating the `ADDRESS_GEOCODER_PROVIDER` setting. For example, to use Scourgify:

```python
ADDRESS_GEOCODER_PROVIDER = "scourgify"  # Use Scourgify for address parsing
```

This modular approach allows your application to adapt to different geographic or business requirements without changing your codebase.

---

## Running Tests

To test the package, set up a local environment and run:

```bash
pytest autoparsed_address_field/tests
```

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
