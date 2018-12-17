#!python3

import requests,json,sys,os,datetime, re
from termcolor import colored
from urllib.parse import urlparse, urlsplit, parse_qsl, parse_qs

x = datetime.datetime.now()
rightNow = int(x.strftime("%H%M"))
t_date = x.strftime("%Y-%m-%d")
#rightMinute = int(rightNow.st)
#print(rightNow)

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
	
url= "https://api.iextrading.com/1.0/stock/" + str(qString.upper()) +"/batch?types=quote,chart&range=1m"
response = requests.get(url) #gets info
parse = urlparse(url) #prints> ParseResult(scheme='https', netloc='api.iextrading.com', path='/1.0/stock/market/batch', params='', query='symbols=V,FB,NBIX&types=quote', fragment='')
#querystringl = parse_qsl(parse.query) #prints> [('symbols', 'V,FB,NBIX'), ('types', 'quote')]
querystring = parse_qs(parse.query)  #prints> {'symbols': ['V,FB,NBIX'], 'types': ['quote']}
parsed = json.loads(response.text) #json.loads will parse data from response.text, has option to format. ex: json.loads(response.text, indent=4)
#print(json.dumps(parsed, indent=2))
#print(len(parsed['chart']))
#symbolsList=querystring['symbols'][0].split(',')
#print(parsed['chart'][3]['changePercent'])
#sys.exit()	

print(f"{qString.upper():<10}")
print(f"{'Date':>10}{'Close':>10}{'Change %':>10}{'Volume':>15}{'AvgVolume':>15}")
t_price = f"{parsed['quote']['latestPrice']:.2f}".join('$ ')
t_chgPct = f"{parsed['quote']['changePercent']:.2f}".join(' %') 
t_vol = parsed['quote']['latestVolume']
t_vol1 = f"{parsed['quote']['latestVolume']:,}"
t_avgVol = parsed['quote']['avgTotalVolume']
t_chgVol = f"{(t_vol/t_avgVol):.0%}"
print(f"{t_date:<10}{t_price:>10}{t_chgPct:>10}{t_vol1:>15}{t_chgVol:>15}")
for i in range((len(parsed['chart'])-1),-1,-1):
    date = f"{parsed['chart'][i]['date']}"
    close = f"{parsed['chart'][i]['close']:.2f}".join('$ ') 
    x = str(parsed['chart'][i]['changePercent'])
    if x.startswith("-"):
        chgPct = colored(f"{parsed['chart'][i]['changePercent']:.2f}".join(' %'),'red')
    else:
        chgPct = colored(f"{parsed['chart'][i]['changePercent']:.2f}".join(' %'),'green')
    chgPct.strip 
    vol= f"{parsed['chart'][i]['volume']:,}" 
    chgVol = f"{(parsed['chart'][i]['volume']/t_avgVol):.0%}"
    print(f"{date:<10}{close:>10}{chgPct:>10}{vol:>15}{chgVol:>15}")

#day1 = f"{parsed['chart'][0]['close']}"
#print(f"{price:>10}\n")
#print(f"{day1:>10}\n")
sys.exit()	
