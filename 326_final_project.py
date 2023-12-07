"""
Welcome to our Final Project: Currency Converter

Zafir Kazi, David Zannou, Max Eliker, Andrew Bian
"""
import requests
from forex_python.converter import CurrencyRates
import tkinter as tk
from tkinter import OptionMenu, Label, Entry, Button, StringVar

100
api_key = 'YOUR_API_KEY'

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

def perform_conversion():
    base_currency = base_currency_var.get()
    target_currency = target_currency_var.get()

    exchange_rate = get_exchange_rate(api_key, base_currency, target_currency)

    if exchange_rate is not None:
        amount_to_convert = float(amount_entry.get())
        result = convert_currency(amount_to_convert, exchange_rate)
        result_label.config(text=f"{amount_to_convert} {base_currency} is equal to {result:.2f} {target_currency}")
    else:
        result_label.config(text="Currency conversion failed.")

# Tkinter GUI setup
app = tk.Tk()
app.title("Currency Converter")

# Variables for storing user input
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
OptionMenu(app, base_currency_var, "USD", "EUR", "GBP", "CNY", "CHF", "JOD").grid(row=1, column=1, padx=10, pady=5)
OptionMenu(app, target_currency_var, "USD", "EUR", "GBP", "CNY", "CHF", "JOD").grid(row=2, column=1, padx=10, pady=5)

# Button
convert_button = Button(app, text="Convert", command=perform_conversion)
convert_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result label
result_label = Label(app, text="", font=("Helvetica", 12))
result_label.grid(row=4, column=0, columnspan=2, pady=5)

# Run the Tkinter main loop
app.mainloop()
