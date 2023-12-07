"""
Welcome to our Final Project: Currency Converter

Zafir Kazi, David Zannou, Max Eliker, Andrew Bian
"""
import requests
from forex_python.converter import CurrencyRates

def get_exchange_rate(api_key, base_currency, target_currency):
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    params = {"apikey": api_key}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['rates'].get(target_currency)
    else:
        print(f"Error: Unable to fetch exchange rates. Status code: {response.status_code}")
        return None

def convert_currency(amount, exchange_rate):
    if exchange_rate is not None:
        return amount * exchange_rate
    else:
        return None

def get_user_input():
    amount = float(input("Enter the amount you want to convert: "))
    from_currency = input("Enter the source currency (e.g., USD): ").upper()
    to_currency = input("Enter the target currency (e.g., EUR): ").upper()
    return amount, from_currency, to_currency

def display_result(amount, from_currency, result, to_currency):
    print(f"{amount} {from_currency} is equal to {result:.2f} {to_currency}")

def currency_converter():
    api_key = 'YOUR_API_KEY'
    base_currency = 'USD'
    target_currency = 'EUR'

    exchange_rate = get_exchange_rate(api_key, base_currency, target_currency)

    if exchange_rate is not None:
        amount_to_convert, from_currency, to_currency = get_user_input()

        result = convert_currency(amount_to_convert, exchange_rate)

        display_result(amount_to_convert, from_currency, result, to_currency)
    else:
        print("Currency conversion failed.")

def main():
    print("Welcome to the Currency Converter")
    currency_converter()

if __name__ == "__main__":
    main()
