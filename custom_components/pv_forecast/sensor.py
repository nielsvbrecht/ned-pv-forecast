"""Platform for PV Forecast NED.nl sensor integration."""
from __future__ import annotations

import logging
from typing import Any

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


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the PV Forecast NED.nl sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Create a sensor for each forecast period
    sensors = []
    if coordinator.data and "hydra:member" in coordinator.data:
        for entry in coordinator.data["hydra:member"]:
            sensors.append(
                PVForecastSensor(
                    coordinator,
                    entry["validfrom"],
                    config_entry.entry_id,
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
        timestamp: str,
        entry_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._timestamp = timestamp
        self._entry_id = entry_id
        self._attr_unique_id = f"{entry_id}_{timestamp}"
        self._attr_name = f"PV Forecast NED.nl {timestamp}"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if (
            self.coordinator.data
            and "hydra:member" in self.coordinator.data
        ):
            for entry in self.coordinator.data["hydra:member"]:
                if entry["validfrom"] == self._timestamp:
                    return float(entry["volume"])
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if (
            self.coordinator.data
            and "hydra:member" in self.coordinator.data
        ):
            for entry in self.coordinator.data["hydra:member"]:
                if entry["validfrom"] == self._timestamp:
                    return {
                        "valid_from": entry["validfrom"],
                        "valid_to": entry["validto"],
                    }
        return {}
