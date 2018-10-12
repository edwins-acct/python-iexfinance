import requests
import json
from urllib.parse import urlparse, urlsplit, parse_qsl, parse_qs

#url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"
#url= "https://api.iextrading.com/1.0/stock/nbix/peers"
url= "https://api.iextrading.com/1.0/stock/market/batch?symbols=aapl,fb&types=quote&range=1m&last=2"
response = requests.get(url)
parse = urlparse(url)
querystringl = parse_qsl(parse.query)
querystring = parse_qs(parse.query)
data = response.text
parsed = json.loads(data)
#print(json.dumps(parsed, indent=4))
print(parse.query)
print(querystring['symbols'])
print(response.url)

#date = parsed["date"]
for ticker in data.items():
#	print()
tickers = parsed["AAPL"]["quote"]["symbol"]
print("ticker is " + str(tickers))
#gbp_rate = parsed["rates"]["GBP"]
#usd_rate = parsed["rates"]["USD"]
#print("On " + date + " EUR equals " + str(gbp_rate) + " GBP")
#print("On " + date + " EUR equals " + str(usd_rate) + " USD")