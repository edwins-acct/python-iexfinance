import sys, sqlite3, stocks

def user_inputs():
	'''inputs will be used to query db'''
	user = input("User_id(sch_inv,fid_inv,fid_ira,fid_rira): ")
	name = input("Name of watchlist: ")
	check_watchlist(user,name)


def check_watchlist(user_id,w_name):
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
		action = input("Add to or delete from watchlist: ")
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
	



if __name__ == "__main__":
	global conn
	conn = stocks.db_connect('stocks.db')
	c = conn.cursor()

	user_inputs()

conn.close()
sys.exit()