# PV Forecast NED.nl

This project provides a Home Assistant integration to fetch photovoltaic (PV) generation forecasts for provinces in the Netherlands using the ned.nl API.

## Installation in Home Assistant

There are two ways to install this integration:

### Method 1: HACS (Recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. Go to HACS in your Home Assistant instance
3. Click on "Integrations"
4. Click the "+" button in the bottom right corner
5. Search for "PV Forecast NED.nl"
6. Click "Download"
7. Restart Home Assistant

### Method 2: Manual Installation

1. Copy the `custom_components/pv_forecast` directory from this repository
2. Paste it into your Home Assistant's `custom_components` directory
3. Restart Home Assistant

### Configuration

After installation:

1. Go to Settings → Devices & Services
2. Click "+ ADD INTEGRATION"
3. Search for "PV Forecast NED.nl"
4. Fill in the required information:
   * Your NED.nl API key
   * Province
   * Days to forecast (1-7)
   * Data granularity (10 minutes, 15 minutes, Hour, or Day)

The integration will create sensors showing the forecasted PV generation for your selected province.

## Standalone Usage

If you want to use this as a standalone Python script instead of a Home Assistant integration, check out the [standalone branch](https://github.com/nielsvbrecht/ned-pv-forecast/tree/standalone).

## API Information

This project interacts with the ned.nl API to retrieve photovoltaic generation forecasts. Ensure you have the necessary API access and credentials if required.

## Status

[![Docker Publish](https://github.com/nielsvbrecht/ned-pv-forecast/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/nielsvbrecht/ned-pv-forecast/actions/workflows/docker-publish.yml)

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.