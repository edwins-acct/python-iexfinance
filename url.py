import requests,json,sys
import pandas as pd 
from urllib.parse import urlparse, urlsplit, parse_qsl, parse_qs

#url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"
#url= "https://api.iextrading.com/1.0/stock/nbix/peers"
#url= "https://api.iextrading.com/1.0/stock/market/batch?symbols=aapl,fb&types=quote&range=1m&last=2"
file = open("C:\\Users\erobles3\Desktop\\config.txt", "r")
fileContent = file.read()
file.close()
fileContent=fileContent.replace('\n',',')
print(fileContent)
url= "https://api.iextrading.com/1.0/stock/market/batch?symbols=" + str(fileContent) +"&types=quote"
url1= "https://api.iextrading.com/1.0/stock/market/batch?symbols=AAPL&types=price,news"
print(url)
response = requests.get(url)
parse = urlparse(url)
querystringl = parse_qsl(parse.query)
querystring = parse_qs(parse.query)
data = response.text
parsed = json.loads(data)
#print(json.dumps(parsed))
print(json.dumps(parsed, indent=4))

#print(data)
#print(parse.query)
hereis=querystring['symbols'][0].split(',')
#print(parsed['AAPL']['quote']['ytdChange'])
#print(parsed['FB']['quote']['ytdChange'])
#print(response.url)
#hereis = querystring['symbols']
#hereis1 = hereis.split(',')
#print(hereis[0].split(','))
#date = parsed["date"]
api_call = 'https://api.iextrading.com/1.0/stock/aapl/chart/1d?chartInterval=5' 
price = pd.read_json(api_call)
#df = pd.read_json(url)
print(price)
sys.exit()
for ticker in hereis:
	ticker = ticker.upper()
#	print("company: " + str(parsed[ticker]['quote']['companyName']), end=" ,")
	print("ticker: " + str(ticker), end=" ,")
	print("closing price: " + str(parsed[ticker]['quote']['iexRealtimePrice']), end=" ,")
	print("change $: " + str(parsed[ticker]['quote']['change']), end=" ,")
	print("change %: " + str(parsed[ticker]['quote']['changePercent']), end=" ,")
	print("volume: " + str(parsed[ticker]['quote']['latestVolume']), end=" ,")
	print("avgVolume: " + str(parsed[ticker]['quote']['avgTotalVolume']))
	#print(" is " + str(data))
#tickers = parsed["AAPL"]["quote"]["symbol"]
#print("ticker is " + str(tickers))
#gbp_rate = parsed["rates"]["GBP"]
#usd_rate = parsed["rates"]["USD"]
#print("On " + date + " EUR equals " + str(gbp_rate) + " GBP")
#print("On " + date + " EUR equals " + str(usd_rate) + " USD")
