
"""Test PVForecastSensor compatibility with Python 3.13 and Home Assistant 2025.7"""
from datetime import datetime, timedelta
from custom_components.pv_forecast.sensor import PVForecastSensor, FORECAST_PERIODS
from custom_components.pv_forecast.coordinator import PVForecastDataUpdateCoordinator

class MockCoordinator(PVForecastDataUpdateCoordinator):
    """Mock coordinator for testing PVForecastSensor."""
    def __init__(self, data):
        super().__init__(hass=None, api_key="test", province="Groningen")
        self.data = data
    async def _async_update_data(self):
        """Mock async update data."""
        return self.data


def make_entry(validfrom, validto, volume):
    """Create a mock API entry."""
    return {
        "validfrom": validfrom,
        "validto": validto,
        "volume": volume,
    }



def test_native_value_and_attributes_today():
    """Test native_value and extra_state_attributes for today."""
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
    """Test native_value and attributes when no data is present."""
    coordinator = MockCoordinator({})
    sensor = PVForecastSensor(
        coordinator=coordinator,
        period_id="today",
        days_ahead=0,
        period_name="Today",
        entry_id="test"
    )
    assert sensor.native_value is None
    assert not sensor.extra_state_attributes["hourly_data"]


def test_forecast_periods_dict():
    """Test forecast periods dict for Home Assistant compatibility."""
    assert set(FORECAST_PERIODS.keys()) == {
        "today", "tomorrow", "in_2_days", "in_3_days", "in_4_days", "in_5_days", "in_6_days"
    }
    for info in FORECAST_PERIODS.values():
        assert isinstance(info["days"], int)
        assert isinstance(info["name"], str)
