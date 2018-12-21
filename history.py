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
querystring = parse_qs(parse.query)  #prints> {'symbols': ['V,FB,NBIX'], 'types': ['quote']}
parsed = json.loads(response.text) #json.loads will parse data from response.text, has option to format. ex: json.loads(response.text, indent=4
#print(json.dumps(parsed, indent=2))
#print(len(parsed['chart']))
#sys.exit()	

print(f"{qString.upper():<10}")
print(f"{'Date':>10}{'Close':>10}{'Change $':>10}{'Change %':>10}{'Volume':>12}{'AvgVol':>10}")
t_price = f"{parsed['quote']['latestPrice']:.2f}".join('$ ')
x = str(parsed['quote']['change'])
#x = str(parsed['quote']['changePercent'])
if x.startswith("-"): 
    t_chg= colored(f"{parsed['quote']['change']:.2f}".join('$ '),'red')
    t_chgPct = colored(f"{(parsed['quote']['changePercent']*100):.2f}".join(' %'),'red') #multiply by 100 before adding %
else:
    t_chg= colored(f"{parsed['quote']['change']:.2f}".join('$ '),'green')
    t_chgPct = colored(f"{(parsed['quote']['changePercent']*100):.2f}".join(' %'),'green') #multiply by 100 before adding %
t_vol = parsed['quote']['latestVolume']
t_vol1 = f"{parsed['quote']['latestVolume']:,}"
t_avgVol = parsed['quote']['avgTotalVolume']
t_chgVol = f"{(t_vol/t_avgVol):.0%}"
print(f"{t_date:<10}{t_price:>10}{t_chg:>20}{t_chgPct:>20}{t_vol1:>12}{t_chgVol:>10}")
#for i in range(0,len(parsed['chart'])): #in descending order
for i in range((len(parsed['chart'])-1),-1,-1): #in ascending order
    date = f"{parsed['chart'][i]['date']}"
    close = f"{parsed['chart'][i]['close']:.2f}".join('$ ') 
    x = str(parsed['chart'][i]['change'])
    #x = str(parsed['chart'][i]['changePercent'])
    if x.startswith("-"):
        chg= colored(f"{parsed['chart'][i]['change']:.2f}".join('$ '),'red')
        chgPct = colored(f"{parsed['chart'][i]['changePercent']:.2f}".join(' %'),'red')
    else:
        chg= colored(f"{parsed['chart'][i]['change']:.2f}".join('$ '),'green')
        chgPct = colored(f"{parsed['chart'][i]['changePercent']:.2f}".join(' %'),'green')
    chgPct.strip 
#    print(repr(chgPct))  #prints special characters;normally invisible
    vol= f"{parsed['chart'][i]['volume']:,}" 
    chgVol = f"{(parsed['chart'][i]['volume']/t_avgVol):.0%}"
    print(f"{date:<10}{close:>10}{chg:>20}{chgPct:>20}{vol:>12}{chgVol:>10}")

#day1 = f"{parsed['chart'][0]['close']}"
#print(f"{price:>10}\n")
#print(f"{day1:>10}\n")
sys.exit()	
