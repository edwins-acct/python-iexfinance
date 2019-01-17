import sqlite3,fid_ira,fid_inv,fid_rira

conn = sqlite3.connect('/home/erobles1210/projects/python-iexfinance/stocks.db')
c = conn.cursor()

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
c.executemany('INSERT INTO history(user_id,date,trans,symbol,qty,price) VALUES (?,?,?,?,?,?)',ld)
c.executemany('INSERT INTO history(user_id,date,trans,symbol,qty,price) VALUES (?,?,?,?,?,?)',lx)
c.executemany('INSERT INTO history(user_id,date,trans,symbol,qty,price) VALUES (?,?,?,?,?,?)',lz)

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
