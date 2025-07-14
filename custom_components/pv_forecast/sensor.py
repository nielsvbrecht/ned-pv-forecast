"""Platform for PV Forecast NED.nl sensor integration."""
from __future__ import annotations

import logging
from typing import Any
from datetime import datetime, timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN
from .coordinator import PVForecastDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# Define forecast periods
FORECAST_PERIODS = {
    "today": {"days": 0, "name": "Today"},
    "tomorrow": {"days": 1, "name": "Tomorrow"},
    "in_2_days": {"days": 2, "name": "In 2 Days"},
    "in_3_days": {"days": 3, "name": "In 3 Days"},
    "in_4_days": {"days": 4, "name": "In 4 Days"},
    "in_5_days": {"days": 5, "name": "In 5 Days"},
    "in_6_days": {"days": 6, "name": "In 6 Days"},
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the PV Forecast NED.nl sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Create a fixed set of forecast sensors
    sensors = []
    for period_id, period_info in FORECAST_PERIODS.items():
        sensors.append(
            PVForecastSensor(
                coordinator=coordinator,
                period_id=period_id,
                days_ahead=period_info["days"],
                period_name=period_info["name"],
                entry_id=config_entry.entry_id,
            )
        )

    async_add_entities(sensors, True)


class PVForecastSensor(CoordinatorEntity, SensorEntity):
    """Representation of a PV Forecast NED.nl sensor."""

    _attr_native_unit_of_measurement = "kWh"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL

    def __init__(
        self,
        coordinator: PVForecastDataUpdateCoordinator,
        *,  # Force remaining arguments to be keyword-only
        period_id: str,
        days_ahead: int,
        period_name: str,
        entry_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._period_id = period_id
        self._days_ahead = days_ahead
        self._entry_id = entry_id
        self._attr_unique_id = f"{entry_id}_{period_id}"
        self._attr_name = f"PV Forecast NED.nl {period_name}"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data or "hydra:member" not in self.coordinator.data:
            return None

        # Calculate the date we're looking for
        target_date = datetime.now().date() + timedelta(days=self._days_ahead)
        daily_total = 0.0

        # Sum up all values for the target date
        for entry in self.coordinator.data["hydra:member"]:
            entry_date = datetime.fromisoformat(entry["validfrom"]).date()
            if entry_date == target_date:
                daily_total += float(entry["volume"])

        return daily_total if daily_total > 0 else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        target_date = datetime.now().date() + timedelta(days=self._days_ahead)
        entries = []

        if self.coordinator.data and "hydra:member" in self.coordinator.data:
            for entry in self.coordinator.data["hydra:member"]:
                entry_date = datetime.fromisoformat(entry["validfrom"]).date()
                if entry_date == target_date:
                    entries.append(
                        {
                            "valid_from": entry["validfrom"],
                            "valid_to": entry["validto"],
                            "volume": entry["volume"],
                        }
                    )

        return {
            "forecast_date": target_date.isoformat(),
            "period_name": FORECAST_PERIODS[self._period_id]["name"],
            "hourly_data": entries,
        }
