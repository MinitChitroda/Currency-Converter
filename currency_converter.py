from requests import get
from pprint import PrettyPrinter
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

BASE_URL = "https://api.freecurrencyapi.com/v1/latest"
API_KEY = config["FREE_CURRENCY_API_KEY"]  

printer = PrettyPrinter()  # Gives output in JSON format

def get_currency():
    # Correct the URL construction
    url = f"{BASE_URL}?apikey={API_KEY}"
    data = get(url).json()['data']
    
    data = list(data.items())
    
    data.sort()

    return data


def print_currency(currencies):
    for currency in currencies:
        # currency is a tuple (currency_code, exchange_rate)
        currency_code, rate = currency
        
        # Print currency information
        print(f"Currency Code: {currency_code} | Rate: {rate}")

def exchange_rate(curr1, curr2):
    # Construct the URL to get exchange rate for the specific currency pair
    url = f"{BASE_URL}?apikey={API_KEY}&base_currency={curr1}&symbols={curr2}"
    response = get(url)

    if response.status_code == 200:
        data = response.json()
        # Check if exchange rate data exists for the given pair
        if 'data' in data and curr2 in data['data']:
            rate = data['data'][curr2]
            print(f"Exchange rate from {curr1} to {curr2}: {rate}")
            return rate  # Return just the rate
        else:
            print(f"Error: No exchange rate data found for {curr1} to {curr2}")
    else:
        print(f"Error: Unable to fetch exchange rate (status code: {response.status_code})")

    return None  # Return None if no rate is found

    

def convert(curr1, curr2, amt):
    rate =  exchange_rate(curr1, curr2)
    if rate is None:
        return 

    try:
        amt = float(amt)
    except:
        print("Invalid amount!")
        return
    
    converted_amt = rate * amt
    print(f"{amt} {curr1} = {converted_amt} {curr2}")



def main():
    currencies = get_currency()
    print("Welcome to the currency converter!")
    print("List- Lists the different currencies with their codes and rates")
    print("Convert - Convert from one currency to another")
    print("Rate - get the exchange rate of the two currencies")
    print()

    while True:
        cmd = input("Enter a commad (q to quit): ").lower()

        if cmd == 'q':
            break
        elif cmd == "list":
            print_currency(currencies)
        elif cmd == "convert":
            curr1 = input("Enter base Currency code: ").upper()
            amt = input(f"Enter an anoumt in {curr1}: ")
            curr2 = input("Enter the Currency code u wanna exchange to: ").upper()
            convert(curr1, curr2, amt)
        elif cmd == "rate":
            curr1 = input("Enter a base currency: ").upper()
            curr2 = input("Enter the Currency code u wanna exchange to: ").upper()
            exchange_rate(curr1, curr2)
        else:
            print("Unrecognised Command.")


main()
