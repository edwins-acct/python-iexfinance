import os, sys

name = input("name of portfolio: ")
name += ".txt"
symbol = input("name of symbol(s): ")
print("adding " + symbol + "...")
symbol=symbol.replace(" ","\n")

if os.path.isfile(name):
    with open(name,'a') as file:
        file.write(symbol + "\n")
else:
    with open(name,'w') as file:
        file.write(symbol + "\n")

with open(name,'r') as file:
    #print(file.read())
    x=file.read()
    x=x.replace("\n"," ")
    print("portfolio: "+ x)
#sys.exit()
