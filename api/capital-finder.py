from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        url_components = parse.urlsplit(s)
        query_string_list = parse.parse_qsl(url_components.query)
        dic = dict(query_string_list)

        if "capital" in dic:
            url = "https://restcountries.com/v3.1/capital/"
            r = requests.get(url + dic["capital"])
            data = r.json()
            country = data[0]["name"]["common"]
            message = str(country)
            # results = []
            # for capital_data in data:
            #     result = capital_data["name"][0]["common"][0]
            #     results.append(result)

        if "country" in dic:
            url = "https://restcountries.com/v3.1/name/"
            r = requests.get(url + dic["country"])
            data = r.json()
            capital = data[0]["capital"][0]
            message = str(capital)
            # results = []
            # for country_data in data:
            #     result = country_data["capital"][0]
            #     results.append(result)

        message = "welcome to the capital/country endpoint"

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()

        self.wfile.write(message.encode())

        return
