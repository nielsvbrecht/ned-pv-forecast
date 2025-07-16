"""Test PVForecastSensor compatibility with Python 3.13 and Home Assistant 2025.7"""
import pytest
from datetime import datetime, timedelta
from custom_components.pv_forecast.sensor import PVForecastSensor, FORECAST_PERIODS


from custom_components.pv_forecast.coordinator import PVForecastDataUpdateCoordinator
import types

class MockCoordinator(PVForecastDataUpdateCoordinator):
    def __init__(self, data):
        # Bypass parent init
        self.data = data
        self.hass = None
        self.api_key = "test"
        self.province = "Groningen"
        self.days_to_forecast = 7
        self.granularity = "Hour"
        self._logger = None
        self.update_interval = None
    async def _async_update_data(self):
        return self.data

def make_entry(validfrom, validto, volume):
    return {
        "validfrom": validfrom,
        "validto": validto,
        "volume": volume,
    }


def test_native_value_and_attributes_today():
    today = datetime.now().date()
    validfrom = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    validto = (datetime.now() + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0).isoformat()
    entry = make_entry(validfrom, validto, 123.45)
    coordinator = MockCoordinator({"hydra:member": [entry]})
    sensor = PVForecastSensor(
        coordinator=coordinator,
        period_id="today",
        days_ahead=0,
        period_name="Today",
        entry_id="test"
    )
    assert sensor.native_value == 123.45
    attrs = sensor.extra_state_attributes
    assert attrs["forecast_date"] == today.isoformat()
    assert attrs["period_name"] == "Today"
    assert len(attrs["hourly_data"]) == 1
    assert float(attrs["hourly_data"][0]["volume"]) == 123.45


def test_native_value_none_for_missing_data():
    coordinator = MockCoordinator({})
    sensor = PVForecastSensor(
        coordinator=coordinator,
        period_id="today",
        days_ahead=0,
        period_name="Today",
        entry_id="test"
    )
    assert sensor.native_value is None
    assert sensor.extra_state_attributes["hourly_data"] == []

def test_forecast_periods_dict():
    # Validate forecast periods for Home Assistant compatibility
    assert set(FORECAST_PERIODS.keys()) == {
        "today", "tomorrow", "in_2_days", "in_3_days", "in_4_days", "in_5_days", "in_6_days"
    }
    for period, info in FORECAST_PERIODS.items():
        assert isinstance(info["days"], int)
        assert isinstance(info["name"], str)
