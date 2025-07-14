"""Config flow for PV Forecast NED.nl integration."""
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_PROVINCE,
    CONF_DAYS_TO_FORECAST,
    CONF_GRANULARITY,
    DEFAULT_DAYS_TO_FORECAST,
    DEFAULT_GRANULARITY,
    PROVINCE_MAPPING,
    GRANULARITY_OPTIONS,
)

class PVForecastConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PV Forecast NED.nl."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the API key by trying to get data
            valid = await self.hass.async_add_executor_job(
                self._test_api_key, 
                user_input[CONF_API_KEY],
                user_input[CONF_PROVINCE]
            )

            if valid:
                return self.async_create_entry(
                    title=f"PV Forecast NED.nl - {user_input[CONF_PROVINCE]}",
                    data=user_input,
                )
            
            errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_PROVINCE): vol.In(PROVINCE_MAPPING.keys()),
                    vol.Optional(
                        CONF_DAYS_TO_FORECAST, 
                        default=DEFAULT_DAYS_TO_FORECAST
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=7)),
                    vol.Optional(
                        CONF_GRANULARITY, 
                        default=DEFAULT_GRANULARITY
                    ): vol.In(GRANULARITY_OPTIONS),
                }
            ),
            errors=errors,
        )

    def _test_api_key(self, api_key: str, province: str) -> bool:
        """Test if the API key is valid."""
        try:
            # Import here to avoid circular import
            from .coordinator import PVForecastDataUpdateCoordinator
            
            coordinator = PVForecastDataUpdateCoordinator(
                self.hass,
                api_key=api_key,
                province=province,
            )
            return coordinator.test_api_key()
        except Exception:  # pylint: disable=broad-except
            return False
