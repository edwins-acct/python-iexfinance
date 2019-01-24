#!python3

import requests,json,sys,os,datetime, re, sqlite3
from termcolor import colored
from urllib.parse import urlparse, urlsplit, parse_qsl, parse_qs

def db_connect(db="stocks.db"):
    conn = sqlite3.connect(db)
    return conn

def user_inputs():
    '''inputs will be used to query db'''
    user = input("User_id(sch_inv,fid_inv,fid_ira,fid_rira): ")
    name = input("Name of watchlist: ")
    check_watchlist(user,name)


def check_watchlist(user_id,w_name="watch"):
    '''takes inputs from user_inputs and queries db'''
    c.execute('SELECT symbol from watchlist where user_id=? and w_name=?',(user_id,w_name))
    #use fetchone() because fetchall() returns empty tuple not 'None'
    if c.fetchone() is None:    
        edit_watchlist(user_id,w_name)
    else:
        print(f'Current symbols in {w_name}:',end=' ')
        for row in c.fetchall():
            print(row[0],end=' ')

        print('\n')
        action = input("Add to or delete from watchlist, return to skip: ")
        if not action:
            return
        else:
            edit_watchlist(user_id,w_name,action)

def edit_watchlist(user_id,w_name,action="add"):
    '''inputs from check_watchlist() and either adds or delete symbols'''
    action = action.upper()
    symbol = input("Stock symbol(s): ")
    symbol = symbol.replace(',',' ').replace(';',' ').upper() #instead of using replace method 2x
    symbol = set(symbol.split()) #create a set to eliminate dupes
    input_list = () #create an empty tuple to use in loop
    for sym in symbol:
        input_list = input_list + ((user_id,w_name,sym),)       

    #checks by getting first letter of action to minimize any user input errors; default is add
    if action.startswith('D'):
        c.executemany('DELETE FROM watchlist WHERE user_id=? and w_name=? and symbol=?',input_list)
    else:
        # use executemany for efficiency instead of loop; also use IGNORE so it doesn't terminate if duplicate in db
        c.executemany('INSERT OR IGNORE INTO watchlist(user_id,w_name,symbol) VALUES (?,?,?)',input_list)
    
    conn.commit()

def quote_string_from_file(filename="aspire.txt"):
    '''turns file into string of ticker symbols'''
    with open(filename) as file:
        fileContent = file.read()
        string = fileContent.replace('\n',',')
    string = string[:-1] #deletes trailing comma in string
    return string


def get_data(url): 
    '''query api call'''
    response = requests.get(url) #gets info 
    if "Unknown symbol" in response.text: 
        print(response.text) 
        sys.exit() 
    else: 
        parse = urlparse(url) #prints> ParseResult(scheme='https', netloc='api.iextrading.com', path='/1.0/stock/market/batch', params='', query='symbols=V,FB,NBIX&types=quote', fragment='') querystring = parse_qs(parse.query)  #prints> {'symbols': ['V,FB,NBIX'], 'types': ['quote']} 
        parsed = json.loads(response.text) #json.loads will parse data from response.text, has option to format. ex: json.loads(response.text, indent=4 
        
    return parsed


def history(qString): 
    '''gets historical data for last 30 trading days'''
    url= "https://api.iextrading.com/1.0/stock/" + str(qString.upper()) +"/batch?types=quote,chart&range=1m"
    parsed = get_data(url)
    print(f"{qString.upper() + '  Date':>10}{'Close':>10}{'Change $':>10}{'Change %':>10}{'Volume':>12}{'AvgVol':>10}") 
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
        x = str(parsed['chart'][i]['change']) #x = str(parsed['chart'][i]['changePercent']) 
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


def news(qString): 
    '''gets news for symbol'''
    url= "https://api.iextrading.com/1.0/stock/" + str(qString.upper()) +"/news/last/5"
    parsed = get_data(url)
    print("\nNEWS:") 
    for i in range(0, len(parsed)): 
        date = parsed[int(i)]['datetime'] 
        headline = parsed[int(i)]['headline'] 
        source = colored(parsed[int(i)]['source'], 'yellow') 
        url = colored(parsed[int(i)]['url'], 'blue') 
        print(colored(date[:10], 'cyan')+"  "+headline+"  "+source+"\n   "+url)

if __name__ == "__main__": 
    x = datetime.datetime.now() 
    t_date = x.strftime("%Y-%m-%d") 
    # Check if command line input has exactly 3 args
    if len(sys.argv) != 3 : 
        print('Usage: '+ sys.argv[0] + ' <all|news|history> <symbol>\n')
        sys.exit()
#        if os.path.isfile(sys.argv[2]): 
#            qString = quote_string_from_file(sys.argv[2]) 
#        else: 
            #qString = ','.join(sys.argv[2:]) 
#    else: 
#        qString = quote_string_from_file()
    qString = ','.join(sys.argv[2:]) 

    if sys.argv[1] == 'history':
        history(qString)

    if sys.argv[1] == 'news':
        news(qString)

    if sys.argv[1] == 'all':
        history(qString)
        news(qString)

#    history(qString) 
#    news(qString) 
    print("\n") 
    
    sys.exit()	

