from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import requests


def do_currency(country,value):
    currency_names = []
    for x in value.values():
        a = list(x.values())
        currency_names.append(a[0])
    if len(currency_names) < 3:
        currency_string = 'and '.join(str(v) for v in currency_names)
        currency_string = f" {str(country)} has {len(currency_names)} currencies: " + currency_string + "."
    if len(currency_names) >= 3:
        currency_string = ''.join(str(v) for v in currency_names)
        currency_string = f" {str(country)} has {len(currency_names)} currencies: " + currency_string + "."
    if len(currency_names) == 1:
        currency_string = ''.join(str(v) for v in currency_names)
        currency_string = f" {str(country)} has {len(currency_names)} currency: " + currency_string + "."

    return currency_string

def do_capital(dic):
    url = "https://restcountries.com/v3.1/capital/"
    r = requests.get(url + dic["capital"][0])
    data = r.json()
    country = data[0]["name"]["common"]
    currency = data[0]["currencies"]
    currency_string = do_currency(country,currency)
    input_capital = dic["capital"][0].capitalize()
    actual_country = data[0]["name"]["common"].capitalize()

    return f"{dic['capital'][0].capitalize()} is the capital of {str(country)}", currency_string, input_capital, actual_country

def do_country(dic):
    url = "https://restcountries.com/v3.1/name/"
    r = requests.get(url + dic["country"][0])
    data = r.json()
    capital = data[0]["capital"][0]
    country = dic['country'][0].capitalize()
    currency = data[0]["currencies"]
    currency_string = do_currency(country,currency)
    input_country = dic["country"][0].capitalize()
    actual_capital = data[0]["capital"][0].capitalize()

    return f"{country}'s capital is {str(capital)}.", currency_string, input_country, actual_capital


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        query_string_list = parse_qs(urlparse(s).query, keep_blank_values=True)
        dic = dict(query_string_list)

        if len(dic) == 1:

            if "capital" in dic:
                message, currency, unused_val, unused_val = do_capital(dic)
                message = message + currency
                
            elif "country" in dic:
                message, currency, unused_val, unused_val = do_country(dic)
                message = message + currency

        if len(dic) == 2:

            if "capital" in dic:
                message1,currency1, input_capital, actual_country = do_capital(dic)

            if "country" in dic:
                message2,currency2, input_country, actual_capital = do_country(dic)

            message = "Actually " + message1 + " and " + message2 + currency1 + " " + currency2

            if input_country == actual_country and input_capital == actual_capital:
                message = (f"Correct, {input_country}\'s capital is {input_capital} and{currency1}")

        if len(dic) == 0:

            message = "welcome to the capital/country endpoint"

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.wfile.write(message.encode())

        return
