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

## Settings

### Geocoding Provider

Configure the geocoding provider in your `settings.py` file:

```python
ADDRESS_GEOCODER_PROVIDER = "arcgis"  # Options: "arcgis", "scourgify"
```

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
