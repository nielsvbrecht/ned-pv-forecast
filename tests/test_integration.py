"""Tests for Home Assistant integration."""
from unittest.mock import patch
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pv_forecast.const import DOMAIN
from custom_components.pv_forecast.coordinator import PVForecastDataUpdateCoordinator

@pytest.fixture
def mock_api_response():
    """Fixture for mocked API response."""
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

async def test_setup_entry(hass: HomeAssistant, mock_config_entry, mock_api_response):
    """Test setting up the integration."""
    # Create a mock entry
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=mock_config_entry,
        entry_id="test",
    )
    
    # Mock the coordinator's update method
    with patch(
        "custom_components.pv_forecast.coordinator.PVForecastDataUpdateCoordinator._async_update_data",
        return_value=mock_api_response
    ):
        # Add the config entry
        config_entry.add_to_hass(hass)
        # Set up the entry
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        
        # Check that the sensors were created
        state = hass.states.get("sensor.pv_forecast_ned_nl_today")
        assert state is not None
        assert state.state == "250.0"  # Sum of the volumes

async def test_config_flow(hass: HomeAssistant, mock_config_entry):
    """Test the config flow."""
    # Test user step
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"
    
    # Mock successful API validation
    with patch(
        "custom_components.pv_forecast.coordinator.PVForecastDataUpdateCoordinator.test_api_key",
        return_value=True
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            mock_config_entry
        )
        
        assert result["type"] == "create_entry"
        assert result["title"] == f"PV Forecast NED.nl - {mock_config_entry['province']}"
        assert result["data"] == mock_config_entry

async def test_coordinator_update(hass: HomeAssistant, mock_config_entry, mock_api_response):
    """Test the coordinator update."""
    coordinator = PVForecastDataUpdateCoordinator(
        hass,
        api_key=mock_config_entry["api_key"],
        province=mock_config_entry["province"],
    )
    
    # Mock the API response
    with patch(
        "custom_components.pv_forecast.coordinator.requests.get",
        return_value=type("Response", (), {
            "status_code": 200,
            "json": lambda: mock_api_response,
            "raise_for_status": lambda: None
        })
    ):
        await hass.async_add_executor_job(coordinator._async_update_data)
        assert coordinator.data == mock_api_response

@pytest.mark.parametrize("province,expected", [
    ("Groningen", True),
    ("Invalid", False),
])
async def test_province_validation(hass: HomeAssistant, province, expected):
    """Test province validation in config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    
    test_data = {
        "api_key": "test_key",
        "province": province,
        "days_to_forecast": 7,
        "granularity": "Hour",
        "scan_interval": "6 hours"
    }
    
    with patch(
        "custom_components.pv_forecast.coordinator.PVForecastDataUpdateCoordinator.test_api_key",
        return_value=expected
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            test_data
        )
        
        if expected:
            assert result["type"] == "create_entry"
        else:
            assert result["type"] == "form"
            assert result["errors"] == {"base": "invalid_auth"}
