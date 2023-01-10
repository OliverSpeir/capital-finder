from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        query_string_list = parse_qs(urlparse(s).query, keep_blank_values=True)
        dic = dict(query_string_list)

        if len(dic) == 1:

            if "capital" in dic:
                url = "https://restcountries.com/v3.1/capital/"
                r = requests.get(url + dic["capital"][0])
                data = r.json()
                country = data[0]["name"]["common"]
                currency = data[0]["currencies"]
                currency_names = []
                for x in currency.values():
                    a = list(x.values())
                    currency_names.append(a[0])
                currency_string = ' and '.join(str(w) for w in currency_names)
                message = f"{dic['capital'][0]} is the capital of {str(country)}. The currencies are {currency_string}"

            elif "country" in dic:
                url = "https://restcountries.com/v3.1/name/"
                r = requests.get(url + dic["country"][0])
                data = r.json()
                capital = data[0]["capital"][0]
                message = f"The capital of {dic['country'][0]} is {str(capital)}."

        if len(dic) == 2:

            if "capital" in dic:
                url = "https://restcountries.com/v3.1/capital/"
                r = requests.get(url + dic["capital"][0])
                data = r.json()
                actual_country = data[0]["name"]["common"]
                input_capital = dic["capital"][0]
                message1 = f"{dic['capital'][0]} is the capital of {str(actual_country)} "

            if "country" in dic:
                url2 = "https://restcountries.com/v3.1/name/"
                r = requests.get(url2 + dic["country"][0])
                data = r.json()
                input_country = dic["country"][0]
                actual_capital = data[0]["capital"][0]
                message2 = f"The capital of {dic['country'][0]} is {str(actual_capital)}."

            message = "actually " + message1 + "and " + message2

            if input_country == actual_country.lower() and input_capital == actual_capital.lower():
                message = "you are correct"

        if len(dic) == 0:

            message = "welcome to the capital/country endpoint"

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.wfile.write(message.encode())

        return
