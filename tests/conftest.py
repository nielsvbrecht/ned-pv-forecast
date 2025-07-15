"""Fixtures for PV Forecast NED.nl tests."""
from unittest.mock import patch
import pytest

pytest_plugins = "pytest_homeassistant_custom_component"

@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations for all tests."""
    yield

@pytest.fixture
def mock_api_response():
    """Fixture to provide mock API response."""
    return {
        "hydra:member": [
            {
                "validfrom": "2025-07-12T00:00:00+00:00",
                "validto": "2025-07-12T01:00:00+00:00",
                "volume": 100
            },
            {
                "validfrom": "2025-07-12T01:00:00+00:00",
                "validto": "2025-07-12T02:00:00+00:00",
                "volume": 150
            }
        ]
    }

@pytest.fixture
def mock_config_entry():
    """Create a mock config entry."""
    return {
        "api_key": "test_api_key",
        "province": "Groningen",
        "days_to_forecast": 7,
        "granularity": "Hour",
        "scan_interval": "6 hours"
    }
