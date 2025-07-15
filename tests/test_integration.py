"""Tests for Home Assistant integration."""
from unittest.mock import patch
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from custom_components.pv_forecast.const import DOMAIN

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

@pytest.mark.asyncio
async def test_setup(hass: HomeAssistant, mock_api_response):
    """Test the setup of the integration."""
    with patch(
        "custom_components.pv_forecast.coordinator.PVForecastDataUpdateCoordinator._async_update_data",
        return_value=mock_api_response
    ):
        assert await async_setup_component(hass, DOMAIN, {
            DOMAIN: {
                "api_key": "test_api_key",
                "province": "Groningen"
            }
        })
        await hass.async_block_till_done()
        
        # Verify that the sensors are created
        state = hass.states.get("sensor.pv_forecast_ned_nl_today")
        assert state is not None
        assert state.state == "250.0"  # Sum of the volumes

@pytest.mark.asyncio
async def test_config_flow(hass: HomeAssistant):
    """Test the config flow."""
    from custom_components.pv_forecast.config_flow import PVForecastConfigFlow
    
    flow = PVForecastConfigFlow()
    flow.hass = hass
    
    # Test step 1: user input
    result = await flow.async_step_user({
        "api_key": "test_api_key",
        "province": "Groningen",
        "days_to_forecast": 7,
        "granularity": "Hour",
        "scan_interval": "6 hours"
    })
    
    assert result["type"] == "create_entry"
    assert result["title"] == "PV Forecast NED.nl - Groningen"
    assert result["data"] == {
        "api_key": "test_api_key",
        "province": "Groningen",
        "days_to_forecast": 7,
        "granularity": "Hour",
        "scan_interval": "6 hours"
    }
