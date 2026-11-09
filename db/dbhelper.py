from sqlite3 import connect,Connection, Cursor

db:str = "db/school.db"


def get(sql:str,vals:list)->list: 
    conn:Connection
    cursor:Cursor 
    data:list = []
    
    try:
        conn = connect(db)
        cursor = conn.cursor()
        
        cursor.execute(sql,vals)
        data = cursor.fetchall()
    except Exception as e:
        print(f'Connection Error: {e}')
    finally:
        cursor.close()
        conn.close()
    
    return data
        
        
def post(sql:str,vals:list)->bool:
    conn:Connection
    cursor:Cursor 
     
    try:
        conn = connect(db)
        cursor = conn.cursor()
        
        cursor.execute(sql,vals)
        conn.commit()
        
    except Exception as e:
        print(f'Connection Error: {e}')
    finally:
        cursor.close()
        conn.close()
    return cursor.rowcount > 0

def getAll(table:str): 
    sql:str = f'SELECT * FROM {table}'
    return get(sql,[])

def addRecord(table:str, **kwargs):
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    [flds.append("`"+key+"`") for key in keys]
    fld:str = ",".join(flds)
    qs:list = ['?']*len(vals)
    qmarks:str = ','.join(qs)
    sql:str = f"INSERT INTO {table} ({fld}) VALUES ({qmarks})"
    return post(sql,vals)

def getRecord(table:str,**kwargs):
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    [flds.append("`"+key+"`=?") for key in keys]
    fld:str = " AND ".join(flds)
    sql:str = f"SELECT * FROM {table} WHERE {fld}"
    return get(sql,vals)

def updateRecord(table:str,**kwargs):
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    newvals:list = []
    for i in range(1,len(keys)):
        flds.append("`"+keys[i]+"`=?")
        newvals.append(vals[i])
    sql:str = f"UPDATE {table} SET {",".join(flds)} WHERE `{keys[0]}`= {vals[0]}"
    return post(sql,newvals)

def deleteRecord(table:str,**kwargs):
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    [flds.append("`"+key+"`=?") for key in keys]
    fld:str = " AND ".join(flds)
    sql:str = f"DELETE FROM {table} WHERE {fld}"
    return post(sql,vals)
