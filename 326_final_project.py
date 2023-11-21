"""
Welcome to our Final Project: Currency Converter

Zafir Kazi, David Zannou, Max Eliker, Andrew Bian
"""
import requests

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

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual API key from Open Exchange Rates
    api_key = 'YOUR_API_KEY'
    
    # Define the base and target currencies
    base_currency = 'USD'
    target_currency = 'EUR'

    # Get the exchange rate
    exchange_rate = get_exchange_rate(api_key, base_currency, target_currency)

    if exchange_rate is not None:
        # Input the amount to convert
        amount_to_convert = float(input(f"Enter the amount in {base_currency}: "))

        # Perform the currency conversion
        converted_amount = convert_currency(amount_to_convert, exchange_rate)

        # Display the result
        print(f"{amount_to_convert} {base_currency} is equal to {converted_amount:.2f} {target_currency}")
    else:
        print("Currency conversion failed.")
