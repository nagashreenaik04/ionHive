import random
import string
from faker import Faker
from faker.providers import BaseProvider


class DeviceDataProvider(BaseProvider):

    def charger_id(self, min_length=1, max_length=14):
        length = random.randint(min_length, max_length)
        allowed_chars = string.ascii_letters + string.digits
        return ''.join(random.choices(allowed_chars, k=length))

    def vendor(self, min_length=1, max_length=20):
        length = random.randint(min_length, max_length)
        # Using letters and spaces for vendor names
        name = ''.join(random.choices(string.ascii_letters + " ", k=length)).strip()
        # Ensure at least 1 character
        if len(name) == 0:
            name = random.choice(string.ascii_uppercase)
        return name

    def max_current(self):
        return random.randint(1, 32)

    def max_power(self):
        return random.randint(1, 22000)

    def charger_model(self):
        """Return one of the allowed charger models."""
        return random.choice(['3.5 KW', '7.4 KW', '11 KW', '22 KW'])

    def charger_type(self):
        """Return either 'AC' or 'DC'."""
        return random.choice(['AC', 'DC'])

    def wifi_module(self):
        """Return True or False for WiFi module presence."""
        return random.choice([True, False])

    def bluetooth(self):
        """Return True or False for Bluetooth presence."""
        return random.choice([True, False])

    def connector_type(self):
        """Return either 'Gun' or 'Socket'"""
        return random.choice(['Gun', 'Socket'])