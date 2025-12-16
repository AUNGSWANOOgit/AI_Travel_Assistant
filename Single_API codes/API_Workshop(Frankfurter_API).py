import requests


def convert_currency():
    print("--- Currency Converter (Frankfurter API) ---")

    # 1. Get user inputs
    # .upper() ensures the API recognizes the code (e.g., 'usd' becomes 'USD')
    base_currency = input("Enter the base currency (e.g., USD, EUR): ").upper()
    target_currency = input(
        "Enter the target currency (e.g., JPY, GBP): ").upper()

    try:
        amount = float(input(f"Enter amount in {base_currency}: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    # 2. Construct the URL dynamically using f-strings
    url = f"https://api.frankfurter.dev/v1/latest?base={base_currency}&symbols={target_currency}"

    try:
        # 3. Make the request
        response = requests.get(url)

        # Check if the API call was successful (Status Code 200)
        if response.status_code == 200:
            data = response.json()

            # Check if the target currency exists in the response
            if target_currency in data['rates']:
                rate = data['rates'][target_currency]
                total = rate * amount

                # .2f formats the number to 2 decimal places
                print(
                    f"\nResult: {amount} {base_currency} = {total:.2f} {target_currency}"
                )
                print(
                    f"Exchange Rate: 1 {base_currency} = {rate} {target_currency}"
                )
            else:
                print(
                    f"Error: Could not find exchange rate for {target_currency}."
                )

        elif response.status_code == 404:
            print("Error: One of the currency codes you entered is invalid.")
        else:
            print("Error: Unable to fetch data from the API.")

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")


if __name__ == "__main__":
    convert_currency()
