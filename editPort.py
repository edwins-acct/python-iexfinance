import os, sys, sqlite3,datetime

user = input("user(sch_inv,fid_inv,fid_ira,fid_rira): ")
name = input("name of portfolio: ")
#name += ".txt"
#if os.path.isfile(name): 
#    edit = input("add or delete: ")
#    edit = edit.upper()
#    x=set(line.strip() for line in open(name)) 
#
symbol = input("name of symbol(s): ")
symbol = symbol.replace(',',' ').replace(';',' ').upper() #instead of using replace method 2x
symbol=set(symbol.split())
symbol=tuple(symbol)
print(symbol)
conn = sqlite3.connect('stocks.db')
c = conn.cursor()
c.executemany('INSERT INTO watchlist(user_id,w_name,symbol) VALUES (?,?,?)',symbol)
conn.commit()
conn.close()
sys.exit()




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

#import url
#url
#sys.exit()
import sqlite3,fid_ira,fid_inv,fid_rira


#c.execute('CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)')
#CREATE TABLE user (id integer primary key autoincrement, user_id text unique not null, name text not null);
#CREATE TABLE stock (id integer primary key autoincrement, symbol text unique not null, c_name text not null);
#CREATE TABLE watchlist (id integer primary key autoincrement, user_id text not null, w_name text not null,symbol text not null);
#CREATE TABLE history (id integer primary key autoincrement, user_id text not null,date text not null, trans text not null, symbol text not null, qty
#         real, price real, foreign key(user_id) references user(user_id) on delete cascade, foreign key(symbol) references stock(symbol));

# Insert a row of data
ld=fid_ira.stocks.copy()
lx=fid_rira.stocks.copy()
lz=fid_inv.stocks.copy()
c.executemany('INSERT INTO history(user_id,date,trans,symbol,qty,price) VALUES (?,?,?,?,?,?)',lx)
c.executemany('INSERT INTO history(user_id,date,trans,symbol,qty,price) VALUES (?,?,?,?,?,?)',lz)

# Save (commit) the changes

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
