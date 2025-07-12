# pylint: disable=unused-import, duplicate-code
"""Tests for the PV forecast script."""

from datetime import datetime
from unittest.mock import MagicMock

import pytest
import requests

# Import the function to be tested
from src.main import get_pv_forecast

def test_get_pv_forecast_success(mocker):
    """Test that get_pv_forecast fetches data successfully."""
    # Mock the requests.get method
    mock_get = mocker.patch('src.main.requests.get')

    # Configure the mock to return a successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'hydra:member': [
            {'validfrom': '2025-07-12T00:00:00+00:00',
             'validto': '2025-07-12T01:00:00+00:00', 'volume': 100},
            {'validfrom': '2025-07-12T01:00:00+00:00',
             'validto': '2025-07-12T02:00:00+00:00', 'volume': 150},
        ]
    }
    # Simulate no HTTP errors
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Define test data
    province_name = "Groningen"
    api_key = "TEST_API_KEY"
    start_date = datetime(2025, 7, 12)
    end_date = datetime(2025, 7, 13)

    # Call the function
    forecast_data = get_pv_forecast(province_name, api_key, start_date, end_date, granularity_id=5)

    # Assertions
    expected_url = "https://api.ned.nl/v1/utilizations"
    expected_headers = {
        "X-AUTH-TOKEN": api_key,
        "accept": "application/ld+json"
    }
    expected_params = {
        "point": 1, # Groningen's point ID
        "type": 2,
        "classification": 1,
        "granularity": 5,
        "granularitytimezone": 0,
        "activity": 1,
        "validfrom[after]": "2025-07-12",
        "validfrom[strictly_before]": "2025-07-13",
    }

    mock_get.assert_called_once_with(
        expected_url,
        headers=expected_headers,
        params=expected_params,
        timeout=30 # Ensure timeout is passed
    )

    assert forecast_data == {
        'hydra:member': [
            {'validfrom': '2025-07-12T00:00:00+00:00',
             'validto': '2025-07-12T01:00:00+00:00', 'volume': 100},
            {'validfrom': '2025-07-12T01:00:00+00:00',
             'validto': '2025-07-12T02:00:00+00:00', 'volume': 150},
        ]
    }

def test_get_pv_forecast_api_error(mocker):
    """Test that get_pv_forecast handles API errors."""
    # Mock the requests.get method
    mock_get = mocker.patch('src.main.requests.get')

    # Configure the mock to raise an HTTPError
    mock_get.side_effect = requests.exceptions.RequestException(
        "Simulated API Error"
    )

    # Define test data
    province_name = "Friesland"
    api_key = "TEST_API_KEY"
    start_date = datetime(2025, 7, 12)
    end_date = datetime(2025, 7, 13)

    # Call the function
    forecast_data = get_pv_forecast(province_name, api_key, start_date, end_date, granularity_id=5)

    # Assertions
    # Ensure the function returned None on error
    assert forecast_data is None

    # You could also assert that an error message was printed, but that requires
    # mocking sys.stdout, which is a bit more complex for a basic test.

def test_get_pv_forecast_invalid_province(mocker):
    """Test that get_pv_forecast handles invalid province names."""
    # Mock requests.get to ensure it's NOT called
    mock_get = mocker.patch('src.main.requests.get')

    # Define test data with an invalid province
    province_name = "InvalidProvince"
    api_key = "TEST_API_KEY"
    start_date = datetime(2025, 7, 12)
    end_date = datetime(2025, 7, 13)

    # Call the function
    forecast_data = get_pv_forecast(province_name, api_key, start_date, end_date, granularity_id=5)

    # Assertions
    # Ensure the function returned None for an invalid province
    assert forecast_data is None

    # Ensure requests.get was not called
    mock_get.assert_not_called()
