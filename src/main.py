"""A script to fetch photovoltaic generation forecasts using the ned.nl API."""

# Import necessary libraries
import sys
from datetime import datetime, timedelta
import os
import requests

# API_KEY is now passed as a command-line argument
# Define the base URL for the NED.nl API utilizations endpoint
API_URL = "https://api.ned.nl/v1/utilizations"

# Mapping of province names to point IDs (based on API documentation)
PROVINCE_POINT_MAPPING = {
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
    # Add more provinces if needed based on API docs
}

# Mapping of granularity time formats to API IDs
GRANULARITY_MAPPING = {
    "10 minutes": 3,
    "15 minutes": 4,
    "Hour": 5,
    "Day": 6,
}

# Define a function to fetch the PV forecast
def get_pv_forecast(province_name, api_key, start_date, end_date, granularity_id):
    """Fetch the photovoltaic generation forecast for a specific province within a date range."""
    # Get the point ID for the given province name from the mapping
    point_id = PROVINCE_POINT_MAPPING.get(province_name)
    # Check if the province name is valid (found in the mapping)
    if point_id is None:
        # Print an error message if the province is not found
        print(f"Error: Province '{province_name}' not found in mapping.")
        # Return None to indicate an error
        return None

    headers = {
        "X-AUTH-TOKEN": api_key,
        "accept": "application/ld+json" # Or other format if preferred
    }

    # Define the parameters for the API request, using the provided date range
    params = {
        "point": point_id, # Geographic point (province ID)
        "type": 2, # Energy carrier type (2 for Solar based on API docs)
        "classification": 1, # Data classification (1 for Forecast based on API docs)
        "granularity": granularity_id, # Data granularity (5 for Hour based on API docs, adjust if needed)
        "granularitytimezone": 0, # Granularity timezone (0 for UTC)
        "activity": 1, # Activity type (1 for Providing - generation)
        "validfrom[after]": start_date.strftime('%Y-%m-%d'), # Start date (inclusive)
        "validfrom[strictly_before]": end_date.strftime('%Y-%m-%d'), # End date (exclusive)
    }

    # Use a try-except block to handle potential request errors
    try:
        # Send a GET request to the API with the defined headers and parameters
        # Added timeout to prevent hanging
        response = requests.get(API_URL, headers=headers, params=params, timeout=30)
        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()  # Raise an error for bad responses
        # Parse the JSON response and return it
        return response.json()  # Return the JSON response
    # Catch any request exceptions
    except requests.exceptions.RequestException as e:
        # Print an error message including the exception details
        print(f"Error fetching data from ned.nl API: {e}")
        # Return None to indicate an error
        return None

# Define a function to process the fetched forecast data
def process_forecast_data(data):
    """Process the forecast data and extract relevant information."""
    # The structure of the response might be different, adjust parsing accordingly
    # Check if the data is valid and contains the 'hydra:member' key
    # (where forecast entries are located)
    if data and 'hydra:member' in data:
        # Extract the list of forecast entries
        forecast_entries = data['hydra:member']
        # Check if there are any forecast entries
        if forecast_entries:
            # Print a header for the forecast data
            print("PV Forecast Data:")
            # Iterate through each forecast entry
            for entry in forecast_entries:
                # Adjust key names based on actual API response structure
                # Get the 'validfrom' date, defaulting to 'N/A' if not found
                date_from = entry.get('validfrom', 'N/A')
                # Get the 'validto' date, defaulting to 'N/A' if not found
                date_to = entry.get('validto', 'N/A')
                # Get the 'volume' (or 'capacity') data, defaulting to 'N/A' if not found
                volume = entry.get('volume', 'N/A') # Or 'capacity' depending on what you need
                # Print the extracted forecast information for each entry
                print(f"From: {date_from}, To: {date_to}, Volume: {volume} kWh")
        else:
            # Print a message if no forecast data is available
            # for the selected criteria
            print("No forecast data available for the selected province and criteria.")
    else:
        # Print a message for invalid or empty data received
        print("Invalid or empty forecast data received.")

# Define the main function to run the script
def main():
    """Main function to parse arguments and fetch/process PV forecast."""
    # Read configuration from environment variables
    api_key = os.environ.get("API_KEY")
    province = os.environ.get("PROVINCE")
    days_to_forecast_str = os.environ.get("DAYS_TO_FORECAST", "7") # Default to 7 days
    granularity_str = os.environ.get("GRANULARITY", "Hour") # Default to "Hour"

    if not api_key:
        print("Error: API_KEY environment variable not set.")
        sys.exit(1)
    if not province:
        print("Error: PROVINCE environment variable not set.")
        sys.exit(1)

    try:
        days_to_forecast = int(days_to_forecast_str)
        if not 1 <= days_to_forecast <= 7:
            print("Error: DAYS_TO_FORECAST must be an integer between 1 and 7.")
            sys.exit(1)
    except ValueError:
        print("Error: Invalid value for DAYS_TO_FORECAST. Please provide an integer.")
        sys.exit(1)

    # Get granularity ID from string
    granularity_id = GRANULARITY_MAPPING.get(granularity_str)
    if granularity_id is None:
        error_message = (
            f"Error: Invalid value for GRANULARITY: '{granularity_str}'. "
            f"Allowed values are {list(GRANULARITY_MAPPING.keys())}."
        )
        print(error_message)
        sys.exit(1)

    # Calculate the date range based on the determined number of days
    start_date = datetime.now()
    end_date = start_date + timedelta(days=days_to_forecast)

    # Call the get_pv_forecast function to fetch the data with the date range
    forecast_data = get_pv_forecast(province, api_key, start_date, end_date, granularity_id)
    # Call the process_forecast_data function to process and print the data
    process_forecast_data(forecast_data)

# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function to start the script execution
    main()
