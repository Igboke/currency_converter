import requests
import json
from decimal import Decimal


class FetchRateError(Exception):
    """Exception raised for errors when calling the external currency API."""
    pass

class RateNotFoundError(Exception):
    """Exception raised when the specific rate is not found in the API response."""
    pass

class RateCalculationError(Exception):
    """Exception raised for errors during rate conversion or calculation."""
    pass


def fetch_exchange_rate(base_currency, converted_currency, date_str, endpoint_url):
    """
    Fetches the exchange rate from a given external API endpoint.
    Raises specific exceptions on failure. Returns the rate as Decimal on success.
    """
    # print(f"Attempts to fetch rate from: {endpoint_url}")
    try:
        response = requests.get(endpoint_url)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        raise FetchRateError(f"Request failed for {endpoint_url}: {e}") from e
    except json.JSONDecodeError as e:
        # Catch JSON parsing errors
        raise FetchRateError(f"Invalid JSON response from {endpoint_url}: {e}") from e

    rate_data = data.get(base_currency, {}) # Get the inner dictionary for the base currency or default to empty {}
    rate_value = rate_data.get(converted_currency) # Get the rate for the converted currency

    # Check if the rate was found
    if rate_value is None:
        raise RateNotFoundError(f"Rate for {converted_currency} not found under {base_currency} in the response from {endpoint_url}")

    # Convert the  rate value to Decimal for calculation
    try:
        rate_decimal = Decimal(str(rate_value))
        return rate_decimal

    except Exception as e:
         raise RateCalculationError(f"Could not convert raw rate value '{rate_value}' to Decimal: {e}") from e