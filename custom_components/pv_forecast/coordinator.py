"""DataUpdateCoordinator for PV Forecast NED.nl."""
from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
import requests

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    PROVINCE_MAPPING,
    GRANULARITY_MAPPING,
)

_LOGGER = logging.getLogger(__name__)
API_URL = "https://api.ned.nl/v1/utilizations"

class PVForecastDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching PV Forecast NED.nl data."""

    def __init__(
        self,
        hass: HomeAssistant,
        *,
        api_key: str,
        province: str,
        days_to_forecast: int = 7,
        granularity: str = "Hour",
    ) -> None:
        """Initialize."""
        self.api_key = api_key
        self.province = province
        self.days_to_forecast = days_to_forecast
        self.granularity = granularity

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via API."""
        try:
            return await self.hass.async_add_executor_job(self._get_data)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    def _get_data(self) -> dict[str, Any]:
        """Get the latest data from the API."""
        headers = {
            "X-AUTH-TOKEN": self.api_key,
            "accept": "application/ld+json"
        }

        start_date = datetime.now()
        end_date = start_date + timedelta(days=self.days_to_forecast)

        params = {
            "point": PROVINCE_MAPPING.get(self.province),
            "type": 2,  # Solar
            "classification": 1,  # Forecast
            "granularity": GRANULARITY_MAPPING.get(self.granularity, 5),
            "granularitytimezone": 0,
            "activity": 1,
            "validfrom[after]": start_date.strftime('%Y-%m-%d'),
            "validfrom[strictly_before]": end_date.strftime('%Y-%m-%d'),
        }

        response = requests.get(
            API_URL,
            headers=headers,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def test_api_key(self) -> bool:
        """Test if the API key is valid."""
        try:
            self._get_data()
            return True
        except Exception:  # pylint: disable=broad-except
            return False
