#!python3

import requests,json,sys,os,datetime, re
import pandas as pd 
from urllib.parse import urlparse, urlsplit, parse_qsl, parse_qs
from termcolor import colored

x = datetime.datetime.now()
rightNow = int(x.strftime("%H%M"))
#rightMinute = int(rightNow.st)
#print(rightNow)
#sys.exit()	

def quote_string_from_file(filename="aspire.txt"):
    '''turns file into string of ticker symbols'''
    with open(filename) as file:
        fileContent = file.read()
        string = fileContent.replace('\n',',')
    return string;

# Check if command line input
if len(sys.argv) > 1:
    if os.path.isfile(sys.argv[1]):
        qString = quote_string_from_file(sys.argv[1])
    else:
        qString = ','.join(sys.argv[1:])
else: 
        qString = quote_string_from_file()
	
#url= "https://api.iextrading.com/1.0/stock/nbix/peers"
url= "https://api.iextrading.com/1.0/stock/market/batch?symbols=" + str(qString.upper()) +"&types=quote,earnings,stats"#&displayPercent=true"
#url= "https://api.iextrading.com/1.0/stock/market/batch?symbols=" + str(qString.upper()) +"&types=stats"#&displayPercent=true"
response = requests.get(url) #gets info
parse = urlparse(url) #prints> ParseResult(scheme='https', netloc='api.iextrading.com', path='/1.0/stock/market/batch', params='', query='symbols=V,FB,NBIX&types=quote', fragment='')
#querystringl = parse_qsl(parse.query) #prints> [('symbols', 'V,FB,NBIX'), ('types', 'quote')]
querystring = parse_qs(parse.query)  #prints> {'symbols': ['V,FB,NBIX'], 'types': ['quote']}
parsed = json.loads(response.text) #json.loads will parse data from response.text, has option to format. ex: json.loads(response.text, indent=4)
#print(json.dumps(parsed, indent=2))
symbolsList=querystring['symbols'][0].split(',')

if rightNow < 630 or rightNow >= 1300:		
	print(f"{'Ticker':<10}{'Price':>10}{'Change':>10}{'Change %':>10}{'Change YTD%':>12}{'Volume':>15}{'AvgVolume':>15}{'ChgVol':>8}{'MktCap':>10}{'Day Low-High Range':>20}{'ExtPrice':>10}{'ExtChgPct':>10}\n")
	ext = 1
else:
	print(f"{'Ticker':<10}{'Price':>10}{'Change':>10}{'Change %':>10}{'Change YTD%':>12}{'Volume':>15}{'AvgVolume':>15}{'ChgVol':>8}{'MktCap':>10}{'Day Low-High Range':>20}\n")
	ext = 0

for ticker in sorted(symbolsList):
	try:
		price = f"{parsed[ticker]['quote']['latestPrice']:.2f}".join('$ ')
		dayLow = f"{parsed[ticker]['quote']['low']:.2f}".join('$ ')
		dayHigh = f"{parsed[ticker]['quote']['high']:.2f}".join('$ ')
		extPrice = f"{parsed[ticker]['quote']['extendedPrice']:.2f}".join('$ ')
		chgPct = f"{parsed[ticker]['quote']['changePercent']:.2%}"
		vol= f"{parsed[ticker]['quote']['latestVolume']:,}"
		avgVol = f"{parsed[ticker]['quote']['avgTotalVolume']:,}"
		chgVol = f"{(parsed[ticker]['quote']['latestVolume']/parsed[ticker]['quote']['avgTotalVolume']):.0%}"
		chgYtd = f"{parsed[ticker]['quote']['ytdChange']:.2%}"
		tmp_mktCap = f"{(parsed[ticker]['quote']['marketCap']/1000000):.0f}"
		if len(str(tmp_mktCap)) > 3:
			mktCap = f"{int(tmp_mktCap):,}".join(' B')
		else:
			mktCap = f"{int(tmp_mktCap):,}".join(' M')
		change = f"{parsed[ticker]['quote']['change']:.2f}"
		chgPct = "{:.2%}".format(parsed[ticker]['quote']['changePercent'])
#                if change.startswith("-"):
#			change = colored(change,"red")
#                else:
#                        change = colored(change,"green")

		extChgPct = "{:.2%}".format(parsed[ticker]['quote']['extendedChangePercent'])
		#epsReportDate = f"{parsed[ticker]['quote']['EPSReportDate']}"
		if ext == 1:
			print(f"{ticker:<10}{price:>10}{change:>10}{chgPct:>10}{chgYtd:>12}{vol:>15}{avgVol:>15}{chgVol:>8}{mktCap:>10}{dayLow:>10}-{dayHigh:<10}{extPrice:>10}{extChgPct:>10}") #{epsReportDate:>10}")
		else:
			print(f"{ticker:<10}{price:>10}{change:>10}{chgPct:>10}{chgYtd:>12}{vol:>15}{avgVol:>15}{chgVol:>8}{mktCap:>10}{dayLow:>10}-{dayHigh:<10}")
	except Exception:
		print(f"{ticker:<10} Ticker not found")
		#pass
