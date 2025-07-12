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

## Future plans

1. I plan to integrate the postal code PV forecast into this script once this API is made available by ned.nl
2. Develop this into a Home Assistant module to integrate the PV postal code forecast into your Home Assistant environment

## Home Assistant Addon

This project can be used as a Home Assistant addon. Follow these steps to add and configure the addon in your Home Assistant instance.

### Add the Repository

1. In Home Assistant, navigate to **Settings** -> **Add-ons**.
2. Click on the **Add-on Store** button in the bottom right corner.
3. Click on the three vertical dots in the top right corner and select **Repositories**.
4. Add the URL of this GitHub repository (`https://github.com/nielsvbrecht/ned-pv-forecast`) to the list and click **Add**.
5. Close the repositories list.

### Install the Addon

1. The new repository should now appear in the Add-on Store.
2. Find the "PV Forecast" addon and click on it.
3. Click on the **Install** button.

### Configure the Addon

1. After installation, go to the **Configuration** tab of the addon.
2. You will see options corresponding to the `config.json` file:
    - **API Key**: Enter your ned.nl API key here.
    - **Province**: Enter the name of the province for which you want to fetch the forecast.
    - **Days to Forecast**: Enter the number of days for the forecast (1-7).
3. These options are passed to the script as environment variables (`API_KEY`, `PROVINCE`, `DAYS_TO_FORECAST`). The script `src/main.py` has been modified to read these environment variables instead of command-line arguments.
4. Click **Save**.

### Start the Addon

1. Go to the **Info** tab of the addon.
2. Click on the **Start** button.
3. You can check the addon logs in the **Log** tab to see the fetched forecast data.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.