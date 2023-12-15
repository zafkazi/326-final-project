"""
Welcome to our Final Project: Currency Converter

Zafir Kazi, David Zannou, Max Eliker, Andrew Bian
"""
import requests
from forex_python.converter import CurrencyRates
import tkinter as tk
from tkinter import OptionMenu, Label, Entry, Button, StringVar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

api_key = '  API_KEY'

def get_exchange_rate(api_key, base_currency, target_currency):
    """
    Gets exchange rate using an API

    Parameters:
    api_key: accesses the exchange rate
    base_currency: the currency from which one the rate is calculated
    target_currency: the currency to which one the rate is calculated

    Returns: the exchange rate from base_currency to target_currency, otherwise returns None
    """
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
    """
    Converts the amount of money from one currency to the other based on user input
    
    Parameters:
    amount: amount of money that's being converted
    exchange_rate: the exchange rate for said conversion

    Returns: converted amount of money
    """
    if exchange_rate is not None:
        return amount * exchange_rate
    else:
        return None

def get_historical_exchange_rates(api_key, base_currency, target_currency, start_date, end_date):
    url = f"https://open.er-api.com/v6/time-series/{start_date}/{end_date}"
    params = {"apikey": api_key, "base": base_currency, "symbols": target_currency}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        rates = data['rates'][target_currency]
        dates = [datetime.strptime(date, "%Y-%m-%d") for date in rates.keys()]
        values = list(rates.values())
        return pd.DataFrame({"Date": dates, "Exchange Rate": values})
    else:
        print(f"Error: Unable to fetch historical exchange rates. Status code: {response.status_code}")
        return None

def convert_and_plot():
    base_currency = base_currency_var.get()
    target_currency = target_currency_var.get()

    exchange_rate = get_exchange_rate(api_key, base_currency, target_currency)

    if exchange_rate is not None:
        amount_to_convert = float(amount_entry.get())
        result = convert_currency(amount_to_convert, exchange_rate)
        result_label.config(text=f"{amount_to_convert} {base_currency} is equal to {result:.2f} {target_currency}")

        # Plot exchange rate over time
        plot_exchange_rate_over_time(api_key, base_currency, target_currency, "2022-01-01", "2023-01-01")
    else:
        result_label.config(text="Currency conversion failed.")

def plot_exchange_rate_over_time(api_key, base_currency, target_currency, start_date, end_date):
    currencies = ["USD", "EUR", "JPY", "GBP", "AUD"]

    plt.figure(figsize=(12, 8))

    for currency in currencies:
        historical_data = get_historical_exchange_rates(api_key, currency, target_currency, start_date, end_date)

        if historical_data is not None:
            sns.lineplot(x='Date', y='Exchange Rate', data=historical_data, label=f"{currency}/{target_currency}")

    plt.title(f"Exchange Rate Over Time")
    plt.xlabel("Date")
    plt.ylabel("Exchange Rate")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

def rating_best_currencies(api_key):
    """
    Grab the best/strongest currencies based on its current exchange rate

    Parameters:
    api_key: necessary to access the exchange rate amount to determine the best one
    
    Returns:
    best_currencies: list of the best currencies based on rates compared to USD
    """
    currencies = ["USD", "EUR", "JPY", "GBP", "AUD"]
    ratings = {}

    for currency in currencies:
        exchange_rate = get_exchange_rate(api_key, currency, "USD")
        if exchange_rate is not None:
            ratings[currency] = exchange_rate

    best_currencies = sorted(ratings, key=ratings.get, reverse=True)
    return best_currencies

def rating_worst_currencies(api_key):
    """
    Grab the worst/weakest currencies based on its current exchange rate

    Parameters:
    api_key: necessary to access the exchange rate amount to determine the worst one
    
    Returns:
    worst_currencies: list of the worst currencies based on rates compared to USD
    """
    currencies = ["USD", "EUR", "JPY", "GBP", "AUD"]
    ratings = {}

    for currency in currencies:
        exchange_rate = get_exchange_rate(api_key, currency, "USD")
        if exchange_rate is not None:
            ratings[currency] = exchange_rate

    worst_currencies = sorted(ratings, key=ratings.get)
    return worst_currencies

def create_inflation_table(inflation, years):
    """
    Create a line plot that displays the inflation rate for several years

    Parameters:
    inflation: list of rates that correspond to a certain  year
    years: list of years that correspond to certain inflation rate
    """
    data = pd.DataFrame({'Years': years, 'Inflation Rate (5%) ': inflation})
    sns.lineplot(data=data, x=years, y=inflation)
    plt.xlabel('Years')
    plt.ylabel('Inflation Rate (%)')
    plt.title('Inflation Rate Over Time')
    plt.savefig('inflation_plot.png')  # Save the plot as an image file
    plt.show()


inflation = [3.73, 2.62, 2.35, 1.43, 1.55, 2.19, 2.4, 2.21, 1.93, 3.48, 8.27]
years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
create_inflation_table(inflation, years)

# Tkinter GUI setup
"""
Set up a Tkinter currency converter and exchange rate calculator
Conversion tool and plotting of graphs

GUI displays:
-Input fields for conversion amount, base currency, and target currency
-Buttons:
    -inflation rate table
    -rating best and worst currencies
    -conversion of currencies and plotting against rate of exchange
"""
app = tk.Tk()
app.title("Currency Converter and Exchange Rate Plotter")

# Variables for storing user input (make them global)
global base_currency_var
global target_currency_var

base_currency_var = StringVar(app)
base_currency_var.set("USD")
target_currency_var = StringVar(app)
target_currency_var.set("EUR")

# Labels
Label(app, text="Amount to convert:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
Label(app, text="Source currency:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
Label(app, text="Target currency:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

# Entry widgets
amount_entry = Entry(app)
amount_entry.grid(row=0, column=1, padx=10, pady=5)
OptionMenu(app, base_currency_var, "USD", "EUR", "JPY", "GBP", "AUD").grid(row=1, column=1, padx=10, pady=5)
OptionMenu(app, target_currency_var, "USD", "EUR", "JPY", "GBP", "AUD").grid(row=2, column=1, padx=10, pady=5)

# Button to convert
convert_button = Button(app, text="Convert", command=convert_and_plot)
convert_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result label
result_label = Label(app, text="", font=("Helvetica", 12))
result_label.grid(row=4, column=0, columnspan=2, pady=5)

# Button to plot exchange rate over time
plot_button = Button(app, text="Plot Exchange Rate Over Time", command=lambda: plot_exchange_rate_over_time(api_key, base_currency_var.get(), target_currency_var.get(), "2022-01-01", "2023-01-01"))
plot_button.grid(row=5, column=0, columnspan=2, pady=10)

# Button to convert and plot
convert_and_plot_button = Button(app, text="Convert and Plot", command=convert_and_plot)
convert_and_plot_button.grid(row=6, column=0, columnspan=2, pady=10)

# Button to rate best currencies
best_currencies_button = Button(app, text="Rate Best Currencies", command=lambda: show_result(rating_best_currencies(api_key)))
best_currencies_button.grid(row=7, column=0, columnspan=2, pady=10)

# Button to rate worst currencies
worst_currencies_button = Button(app, text="Rate Worst Currencies", command=lambda: show_result(rating_worst_currencies(api_key)))
worst_currencies_button.grid(row=8, column=0, columnspan=2, pady=10)

# Button to create inflation table
inflation_table_button = Button(app, text="Create Inflation Table", command=lambda: show_result(create_inflation_table()))
inflation_table_button.grid(row=9, column=0, columnspan=2, pady=10)

# Function to show the result in a messagebox or any other desired way
def show_result(result):
    if result is not None:
        result_label.config(text=str(result))
    else:
        result_label.config(text="Operation failed.")

# Run the Tkinter main loop
app.mainloop()