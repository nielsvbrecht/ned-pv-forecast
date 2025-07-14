"""The PV Forecast NED.nl integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_PROVINCE,
    CONF_DAYS_TO_FORECAST,
    CONF_GRANULARITY,
    CONF_SCAN_INTERVAL,
)
from .coordinator import PVForecastDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PV Forecast from a config entry."""
    coordinator = PVForecastDataUpdateCoordinator(
        hass,
        api_key=entry.data[CONF_API_KEY],
        province=entry.data[CONF_PROVINCE],
        days_to_forecast=entry.data.get(CONF_DAYS_TO_FORECAST, 7),
        granularity=entry.data.get(CONF_GRANULARITY, "Hour"),
        scan_interval=entry.data.get(CONF_SCAN_INTERVAL, "6 hours"),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
