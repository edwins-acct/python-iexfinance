import sqlite3

db = '/home/erobles1210/projects/python-iexfinance/stocks.db'
con = sqlite3.connect(db)
con.isolation_level = None
cur = con.cursor()

buffer = ""

print("Enter your SQL commands to execute in sqlite3.")
print("Enter a blank line to exit.")

while True: 
    line = input() 
    if line == "": 
        break 

    buffer += line 

    if sqlite3.complete_statement(buffer):  #complete_statement test checks that it's a statement;doesn't check syntax
        try: 
            buffer = buffer.strip() 
            cur.execute(buffer) 

            if buffer.lstrip().upper().startswith("SELECT"): 
                print(cur.fetchall()) 

        except sqlite3.Error as e:  #Error is an attribute of sqlite3 module
            print("An error occurred:", e.args[0]) 
            buffer = "" 
            
con.close()
