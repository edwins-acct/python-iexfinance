import requests,sys,json
from urllib.parse import urlparse, urlsplit, parse_qsl, parse_qs

#url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"
#url= "https://api.iextrading.com/1.0/stock/nbix/peers"
url= "https://api.iextrading.com/1.0/stock/market/batch?symbols=fb&\
types=quote,stats,news&filter=symbol,companyName,latestPrice,change,headline,date,close,change,changePercent,\
day50MovingAvg,day200MovingAvg,priceToSales,priceToBook"
response = requests.get(url)
parse = urlparse(url)
querystringl = parse_qsl(parse.query)
querystring = parse_qs(parse.query)
#data = response.text
#parsed = json.loads(data)
parsed = json.loads(response.text)
print(json.dumps(parsed, indent=4))
#sys.exit()
#print(parse.query)
#print(querystring['symbols'])
#print(querystring['types'])
#print(querystring['filter'])
#print(response.text)

#date = parsed["date"]
#for ticker in data.items():
#	print()
#tickers = parsed["AAPL"]["quote"]["symbol"]
#print("ticker is " + str(tickers))
#gbp_rate = parsed["rates"]["GBP"]
#usd_rate = parsed["rates"]["USD"]
#print("On " + date + " EUR equals " + str(gbp_rate) + " GBP")
#print("On " + date + " EUR equals " + str(usd_rate) + " USD")
