from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.timeseries import TimeSeries
import os
from utils.config import basicconfig
from utils.Colors import Colors
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

API_KEY = basicconfig.ALPHA_VANTAGE_API_KEY

ts = TimeSeries(key=API_KEY, output_format="json")
fd = FundamentalData(key=API_KEY, output_format="json")


crypto_api = CryptoCurrencies(key=API_KEY, output_format='json')
stock_api = TimeSeries(key=API_KEY, output_format='json')


def get_crypto_price(symbol: str, market: str = "USD") -> dict:
    """
    Fetches the most recent daily price data for a cryptocurrency using the Alpha Vantage API.

    Alpha Vantage provides daily OHLCV (Open, High, Low, Close, Volume) data. This function retrieves
    the latest available entry for the given symbol and fiat market (e.g., USD).

    Args:
        symbol (str): The cryptocurrency symbol to fetch (e.g., 'BTC', 'ETH').
        market (str, optional): The fiat currency to compare against (e.g., 'USD'). Defaults to 'USD'.

    Returns:
        dict: A dictionary containing the following keys:
            - symbol (str): The input crypto symbol (in uppercase).
            - market (str): The market currency (in uppercase).
            - open (str): The opening price for the day.
            - high (str): The highest price recorded for the day.
            - low (str): The lowest price recorded for the day.
            - close (str): The closing price for the day.
            - volume (str): The trading volume for the day.
            - timestamp (str): The date of the latest entry (YYYY-MM-DD).

        If an error occurs or no data is found, returns None and logs the error.
    """

    try:
        data, _ = crypto_api.get_digital_currency_daily(symbol=symbol.upper(), market=market.upper())
        if not data:
            print(f'{Colors.BOLD}[{Colors.BRIGHT_RED}ERROR{Colors.RESET}{Colors.BOLD}] No data found for {symbol.upper()}')
            return None

        latest_time = next(iter(data))
        price_data = data[latest_time]

        return {
            "symbol": symbol.upper(),
            "market": market.upper(),
            "open": price_data.get("1. open", "N/A"),
            "high": price_data.get("2. high", "N/A"),
            "low": price_data.get("3. low", "N/A"),
            "close": price_data.get("4. close", "N/A"),
            "volume": price_data.get("5. volume", "N/A"),
            "timestamp": latest_time
        }


    except Exception as e:
        print(f'{Colors.BOLD}[{Colors.BRIGHT_RED}ERROR{Colors.RESET}{Colors.BOLD}] {e}')
        return None



def get_stock_price(symbol: str, market: str = "USD") -> dict:
    """
    Fetches the latest quote for a stock symbol using Alpha Vantage.

    Args:
        symbol (str): The stock symbol to look up (e.g., 'AAPL', 'GOOGL').
        market (str): Optional market currency (default: 'USD').
                      Currently unused — prices are fetched in listing market's currency.

    Returns:
        dict: A dictionary with:
            - symbol (str): The stock symbol
            - open (str): Opening price
            - high (str): Highest price of the day
            - low (str): Lowest price of the day
            - price (str): Current trading price
            - volume (str): Trading volume
            - change_percent (str): % change for the day
            - timestamp (str): Last trading date

        Returns None if data is invalid or an error occurs.
    """
    try:
        data, _ = ts.get_quote_endpoint(symbol=symbol.upper())
        overview, _ = fd.get_company_overview(symbol=symbol.upper())  # <- use FundamentalData here

        if "05. price" not in data:
            print(f'{Colors.BOLD}[{Colors.BRIGHT_RED}ERROR{Colors.RESET}{Colors.BOLD}] Invalid or empty data for {symbol.upper()}{Colors.RESET}')
            return None

        return {
            "symbol": symbol.upper(),
            "name": overview.get("Name", symbol.upper()),  # fallback to symbol if no name
            "open": data["02. open"],
            "high": data["03. high"],
            "low": data["04. low"],
            "price": data["05. price"],
            "volume": data["06. volume"],
            "timestamp": data["07. latest trading day"],
            "change_percent": data["10. change percent"]
        }

    except Exception as e:
        print(f'{Colors.BOLD}[{Colors.BRIGHT_RED}ERROR{Colors.RESET}{Colors.BOLD}] Failed to fetch stock data for {symbol.upper()}: {e}{Colors.RESET}')
        return None

