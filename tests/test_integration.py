"""Tests for Home Assistant integration."""
from unittest.mock import patch
import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pv_forecast.const import DOMAIN
from custom_components.pv_forecast.coordinator import PVForecastDataUpdateCoordinator


async def test_setup_entry(hass: HomeAssistant, mock_config_entry, mock_api_response):
    """Test setting up the integration."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=mock_config_entry,
        entry_id="test",
    )
    with patch(
        "custom_components.pv_forecast.coordinator.PVForecastDataUpdateCoordinator._async_update_data",
        return_value=mock_api_response,
    ):
        config_entry.add_to_hass(hass)
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        state = hass.states.get("sensor.pv_forecast_ned_nl_today")
        assert state is not None
        assert state.state == "250.0"


async def test_config_flow(hass: HomeAssistant, mock_config_entry):
    """Test the config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"
    with patch(
        "custom_components.pv_forecast.coordinator.PVForecastDataUpdateCoordinator.test_api_key",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            mock_config_entry,
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
    with patch(
        "custom_components.pv_forecast.coordinator.requests.get",
        return_value=type("Response", (), {
            "status_code": 200,
            "json": lambda: mock_api_response,
            "raise_for_status": lambda: None,
        }),
    ):
        # pylint: disable=protected-access
        await hass.async_add_executor_job(coordinator._async_update_data)
        assert coordinator.data == mock_api_response


@pytest.mark.parametrize("province,expected", [
    ("Groningen", True),
    ("Invalid", False),
])
async def test_province_validation(hass: HomeAssistant, province, expected, mock_config_entry):
    """Test province validation in config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    test_data = dict(mock_config_entry)
    test_data["province"] = province
    with patch(
        "custom_components.pv_forecast.coordinator.PVForecastDataUpdateCoordinator.test_api_key",
        return_value=expected,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            test_data,
        )
        if expected:
            assert result["type"] == "create_entry"
        else:
            assert result["type"] == "form"
            assert result["errors"] == {"base": "invalid_auth"}
