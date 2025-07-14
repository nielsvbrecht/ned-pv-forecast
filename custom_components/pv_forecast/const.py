"""Constants for the PV Forecast integration."""
from typing import Final
from datetime import timedelta

DOMAIN: Final = "pv_forecast"

# Configuration and options
CONF_API_KEY = "api_key"
CONF_PROVINCE = "province"
CONF_DAYS_TO_FORECAST = "days_to_forecast"
CONF_GRANULARITY = "granularity"
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_DAYS_TO_FORECAST = 7
DEFAULT_GRANULARITY = "Hour"
DEFAULT_SCAN_INTERVAL = timedelta(hours=6)  # 6 hours default

# Scan interval options
SCAN_INTERVAL_OPTIONS = {
    "6 hours": timedelta(hours=6),
    "12 hours": timedelta(hours=12),
    "24 hours": timedelta(hours=24),
}

# Province mapping
PROVINCE_MAPPING = {
    "Groningen": 1,
    "Friesland": 2,
    "Drenthe": 3,
    "Overijssel": 4,
    "Flevoland": 5,
    "Gelderland": 6,
    "Utrecht": 7,
    "Noord-Holland": 8,
    "Zuid-Holland": 9,
    "Zeeland": 10,
    "Noord-Brabant": 11,
    "Limburg": 12,
}

# Granularity mapping
GRANULARITY_OPTIONS = ["10 minutes", "15 minutes", "Hour", "Day"]
GRANULARITY_MAPPING = {
    "10 minutes": 3,
    "15 minutes": 4,
    "Hour": 5,
    "Day": 6,
}
