# PV Forecast Project

This project provides a Python script (`src/main.py`) to fetch photovoltaic (PV) generation forecasts for a specific province in the Netherlands using the ned.nl API. The script allows you to specify the province and an optional date range for the forecast.

## Project Structure

```
pv-forecast-project
├── src
│   └── main.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pv-forecast-project
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the script and obtain the PV generation forecast, you need to provide your ned.nl API key and the name of the province as command-line arguments. Optionally, you can also specify the number of days to forecast.

```bash
python src/main.py <YOUR_ACTUAL_API_KEY> <ProvinceName> [days_to_forecast]
```

*   `<YOUR_ACTUAL_API_KEY>`: Replace this with your actual API key obtained from ned.nl. This is a required argument.
*   `<ProvinceName>`: Replace this with the name of the province for which you want to fetch the forecast (e.g., Groningen, Noord-Holland, etc.). This is a required argument.
*   `[days_to_forecast]`: An optional argument to specify the number of days for the forecast, starting from the current date. If not provided, the script defaults to fetching the forecast for the next 7 days.

**Example:**

To get the PV forecast for the province of Groningen for the next 3 days, run:

```bash
python src/main.py YOUR_API_KEY_HERE Groningen 3
```

To get the PV forecast for the province of Utrecht for the default 7 days, run:

```bash
python src/main.py YOUR_API_KEY_HERE Utrecht
```

## API Information

This project interacts with the ned.nl API to retrieve photovoltaic generation forecasts. Ensure you have the necessary API access and credentials if required.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.