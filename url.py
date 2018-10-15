import requests,json,sys,os
import pandas as pd 
from urllib.parse import urlparse, urlsplit, parse_qsl, parse_qs

#url= "https://api.iextrading.com/1.0/stock/nbix/peers"
#url= "https://api.iextrading.com/1.0/stock/market/batch?symbols=aapl,fb&types=quote&range=1m&last=2"
#file = open("C:\\Users\erobles3\Desktop\\config.txt", "r")
file = open("config.txt","r")
fileContent = file.read()
file.close()
fileContent=fileContent.replace('\n',',')
fileContent= fileContent.upper()
url= "https://api.iextrading.com/1.0/stock/market/batch?symbols=" + str(fileContent) +"&types=quote"#&displayPercent=true"
url1= "https://api.iextrading.com/1.0/stock/market/batch?symbols=AAPL&types=price,news"
#print(url)
response = requests.get(url)
parse = urlparse(url)
querystringl = parse_qsl(parse.query)
querystring = parse_qs(parse.query)
#data = response.text
parsed = json.loads(response.text)
#print(json.loads(response.text, indent=4))
#t= parsed['']
#print(json.dumps(parsed))
#print(json.dumps(parsed, indent=2))
#print(parsed['MSFT'])
#print(parsed)
#print(parse.query)
hereis=querystring['symbols'][0].split(',')
#print(parsed['AAPL']['quote']['ytdChange'])
#print(parsed['FB']['quote']['ytdChange'])
#print(response.url)
#hereis = querystring['symbols']
#hereis1 = hereis.split(',')
#print(hereis[0].split(','))
#date = parsed["date"]
#api_call = 'https://api.iextrading.com/1.0/stock/aapl/chart/1d?chartInterval=5' 
#price = pd.read_json(api_call)
#df = pd.read_json(url)
#print(price)
#sys.exit()
print("{:<10}{:>10}{:>10}{:>10}{:>15}{:>15}{:>15}{:>8}{:>10}".format("Ticker","Price","Change","Change %","Change YTD%","Volume","AvgVolume","ChgVol","MktCap"))
#print(f"Ticker{:<10}Price{:>10}Change{:>10}Change %{:>10}Change YTD%{:>15}Volume{:>15}AvgVolume{:>15}ChgVol{:>8}MktCap{:>10}")
for ticker in hereis:
	price = f"{parsed[ticker]['quote']['latestPrice']:.2f}".join('$ ')
	change = f"{parsed[ticker]['quote']['change']:.2f}"
	chgPct = f"{parsed[ticker]['quote']['changePercent']:.2%}"
	vol= f"{parsed[ticker]['quote']['latestVolume']:,}"
	avgVol = f"{parsed[ticker]['quote']['avgTotalVolume']:,}"
	chgVol = f"{(parsed[ticker]['quote']['latestVolume']/parsed[ticker]['quote']['avgTotalVolume']):.0%}"
	chgYtd = f"{parsed[ticker]['quote']['ytdChange']:.2%}"
	tmp_mktCap = f"{(parsed[ticker]['quote']['marketCap']/1000000):.0f}"
	mktCap = f"{int(tmp_mktCap):,}".join(' B')
#	chgPct = "{:.2%}".format(parsed[ticker]['quote']['changePercent'])
#	vol= "{:,}".format(parsed[ticker]['quote']['latestVolume'])
#	avgVol = "{:,}".format(parsed[ticker]['quote']['avgTotalVolume'])
#	chgVol = "{:.0%}".format(parsed[ticker]['quote']['latestVolume']/parsed[ticker]['quote']['avgTotalVolume'])
#	chgYtd = "{:.2%}".format(parsed[ticker]['quote']['ytdChange'])
	#mktCap = "{:,}".format(int("{0:.0f}".format(parsed[ticker]['quote']['marketCap']/1000000)))
	#mktCap1 = "{:,}".format(int(mktCap))
	#print("{:<10}{:>10}{:>10}{:>10}{:>15}{:>15}{:>15}{:>8}{:>10}".format(ticker, (str(price)).join("$ "), parsed[ticker]['quote']['change'],chgPct,chgYtd, vol, avgVol,chgVol,mktCap.join(" B")))	
	print(f"{ticker:<10}{price:>10}{change:>10}{chgPct:>10}{chgYtd:>15}{vol:>15}{avgVol:>15}{chgVol:>8}{mktCap:>10}")

	#print("ticker: " + str(ticker), end=" ,")
	#print("closing price: " + str(parsed[ticker]['quote']['iexRealtimePrice']), end=" ,")
	#print("change $: " + str(parsed[ticker]['quote']['change']), end=" ,")
	#print("change %: {0:.2%}".format(parsed[ticker]['quote']['changePercent']), end=" ,")
	#print("volume: " + str((parsed[ticker]['quote']['latestVolume']/1000)), end=" ,")
	#print("volume: " + str(vol), end=" ,")
	#print("avgVolume: " + str((parsed[ticker]['quote']['avgTotalVolume']/1000)))
	#print("avgVolume: " + str(avgVol), end=" ,")
	#print("change vol %: + " + str((vol/avgVol)*100))
	#print("change vol %: {0:.0%}".format(vol/avgVol))
	#print(" is " + str(data))
#tickers = parsed["AAPL"]["quote"]["symbol"]
#print("ticker is " + str(tickers))
#gbp_rate = parsed["rates"]["GBP"]
#usd_rate = parsed["rates"]["USD"]
#print("On " + date + " EUR equals " + str(gbp_rate) + " GBP")
#print("On " + date + " EUR equals " + str(usd_rate) + " USD")