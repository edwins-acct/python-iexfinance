import os, sys

name = input("name of portfolio: ")
name += ".txt"
if os.path.isfile(name): 
    edit = input("add or delete: ")
    edit = edit.upper()
    x=set(line.strip() for line in open(name)) 

symbol = input("name of symbol(s): ")
symbol = symbol.replace(',',' ').replace(';',' ').upper() #instead of using replace method 2x
symbol=set(symbol.split())

if os.path.isfile(name): 
    x=set(line.strip() for line in open(name)) 
    if edit.startswith('D'):
        symbol = x - symbol
    else: 
        symbol.update(x) #use if you know both sets are exclusive otherwise use union

symbol = sorted(symbol)
y= " ".join(symbol)
print("portfolio symbol(s): "+ y.upper())

with open(name,'w') as file:
    for sym in symbol:
        file.write(sym.upper() + "\n")

import url
url
#sys.exit()
