# PV Forecast NED.nl

This Home Assistant integration provides forecast data for photovoltaic (PV) energy generation in the Netherlands using the ned.nl API. Get accurate predictions for your province's solar power generation up to 7 days in advance.

![PV Forecast Example](examples/dashboard.png)

## Features

- Province-based PV generation forecasts
- Forecasts available up to 7 days ahead
- Configurable data granularity (10 minutes, 15 minutes, Hour, or Day)
- Adjustable update intervals (6 hours, 12 hours, or daily)
- Easy integration with Home Assistant energy dashboard


## Requirements

**Compatibility:**
- Python 3.13 or newer
- Home Assistant 2025.7.2 or newer

Before installing this integration, you'll need:

1. A ned.nl account with API access
2. An API key from ned.nl
3. Home Assistant 2025.7.2 or newer

## Getting API Access

1. Go to [ned.nl](https://ned.nl) and create an account
2. Navigate to your profile settings
3. Under "API Access", click "Request API Access"
4. Fill in the required information:
   - Organization name
   - Intended use
   - Expected request volume
5. Once approved, you'll receive your API key via email
6. Save this API key, you'll need it during integration setup

## Installation

### HACS (Recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. Go to HACS in your Home Assistant instance
3. Click on "Integrations"
4. Click the "+" button in the bottom right corner
5. Search for "PV Forecast NED.nl"
6. Click "Download"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/pv_forecast` directory from this repository
2. Paste it into your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

After installation:

1. Go to Settings → Devices & Services
2. Click "+ ADD INTEGRATION"
3. Search for "PV Forecast NED.nl"
4. Fill in the required information:
   - Your NED.nl API key
   - Province (choose your province)
   - Days to forecast (1-7)
   - Data granularity (10 minutes, 15 minutes, Hour, or Day)
   - Update interval (6 hours, 12 hours, or once per day)

## Available Sensors

The integration creates the following sensors:

- `sensor.pv_forecast_ned_nl_today`: Today's forecast
- `sensor.pv_forecast_ned_nl_tomorrow`: Tomorrow's forecast
- `sensor.pv_forecast_ned_nl_in_2_days`: Forecast for 2 days ahead
- And so on up to 7 days ahead

Each sensor provides:

- State: Total expected kWh for that day
- Attributes:
  - forecast_date: The date of the forecast
  - period_name: Human-readable name (Today, Tomorrow, etc.)
  - hourly_data: Detailed hourly breakdown of the forecast

## Using the Integration

### Energy Dashboard

Add the forecast to your Energy Dashboard:

1. Go to Energy → Settings
2. Under "Solar Production Forecast", click "Add Solar Production Forecast"
3. Select the "PV Forecast NED.nl Today" sensor

### Example Automations

Here's an example automation that notifies you when tomorrow's forecast is particularly good:

```yaml
automation:
  - alias: "High PV Production Tomorrow"
    trigger:
      - platform: state
        entity_id: sensor.pv_forecast_ned_nl_tomorrow
    condition:
      - condition: numeric_state
        entity_id: sensor.pv_forecast_ned_nl_tomorrow
        above: 20.0  # kWh
    action:
      - service: notify.mobile_app
        data:
          message: "Good solar production expected tomorrow: {{ states('sensor.pv_forecast_ned_nl_tomorrow') }} kWh"
```

## Troubleshooting

### Common Issues

1. **API Key Invalid**
   - Double-check your API key
   - Ensure your API access hasn't expired
   - Contact ned.nl support if issues persist

2. **No Data Available**
   - Check your internet connection
   - Verify the selected province
   - Make sure the update interval has passed

3. **Integration Not Showing Up**
   - Clear your browser cache
   - Restart Home Assistant
   - Check Home Assistant logs for errors

### Debug Logging

To enable debug logs for this integration:

```yaml
logger:
  default: info
  logs:
    custom_components.pv_forecast: debug
```
## Status

[![HACS & Home Assistant Integration Tests](https://github.com/nielsvbrecht/ned-pv-forecast/actions/workflows/hacs_ha_test.yml/badge.svg)](https://github.com/nielsvbrecht/ned-pv-forecast/actions/workflows/hacs_ha_test.yml)

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

## Support

- Report bugs via [GitHub Issues](https://github.com/nielsvbrecht/ned-pv-forecast/issues)
- Join the discussion in the [Home Assistant Community](https://community.home-assistant.io/) forum