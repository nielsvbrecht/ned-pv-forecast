"""A script to fetch photovoltaic generation forecasts using the ned.nl API."""

# Import necessary libraries
import sys
from datetime import datetime, timedelta
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

# Define a function to fetch the PV forecast
def get_pv_forecast(province_name, api_key, start_date, end_date):
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
        "granularity": 5, # Data granularity (5 for Hour based on API docs, adjust if needed)
        "granularitytimezone": 0, # Granularity timezone (0 for UTC)
        "activity": 1, # Activity type (1 for Providing - generation)
        "validfrom[after]": start_date.strftime('%Y-%m-%d'), # Start date (inclusive)
        "validfrom[strictly_before]": end_date.strftime('%Y-%m-%d'), # End date (exclusive)
    }

    # Use a try-except block to handle potential request errors
    try:
        # Send a GET request to the API with the defined headers and parameters
        response = requests.get(API_URL, headers=headers, params=params)
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
    # Check if the correct number of command-line arguments is provided
    # (at least 2 required)
    if len(sys.argv) < 3:
        if len(sys.argv) == 1:
            print("Error: API key and province name are missing.")
        elif len(sys.argv) == 2:
            print("Error: Province name is missing.")
        # Print usage instructions
        print("Usage: python main.py <api_key> <province_name> [days_to_forecast]")
        # Exit the script with an error code
        sys.exit(1)

    # Get the API key from the first command-line argument
    api_key = sys.argv[1]
    # Get the province name from the second command-line argument
    province = sys.argv[2]

    # Determine the number of days to forecast
    days_to_forecast = 7 # Default to 7 days
    if len(sys.argv) > 3:
        try:
            # Attempt to convert the third argument to an integer
            days_to_forecast = int(sys.argv[3])
            # Validate that the number of days is between 1 and 7
            if not 1 <= days_to_forecast <= 7:
                print("Error: Number of days to forecast must be between 1 and 7.")
                print("Usage: python main.py <api_key> <province_name> [days_to_forecast]")
                sys.exit(1)
        except ValueError:
            print("Error: Invalid value for days to forecast. Please provide an integer.")
            print("Usage: python main.py <api_key> <province_name> [days_to_forecast]")
            sys.exit(1)

    # Calculate the date range based on the determined number of days
    start_date = datetime.now()
    end_date = start_date + timedelta(days=days_to_forecast)

    # Call the get_pv_forecast function to fetch the data with the date range
    forecast_data = get_pv_forecast(province, api_key, start_date, end_date)
    # Call the process_forecast_data function to process and print the data
    process_forecast_data(forecast_data)

# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function to start the script execution
    main()