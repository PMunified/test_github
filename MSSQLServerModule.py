import pyodbc
import constants
def connectToMSSQLServer():
    connString = f"DRIVER={constants.ODBC_DRIVER};" \
                 f"SERVER={constants.SERVER_IP};" \
                 f"PORT={constants.PORT_NUM};" \
                 f"DATABASE={constants.DATABASE};" \
                 f"UID={constants.ACCESS_USER};" \
                 f"PWD={constants.PWD};" \
                 f"Trusted Connection=Yes"
    conn = pyodbc.connect(connString)

    return conn;   

def updateNewLaunchItemStatus(item_cd,new_status):
     conn = connectToMSSQLServer()
     cursor = conn.cursor()
     queryString = f"Update MDB_ITEM_MASTER Set MDB_ITEM_MASTER.Status='{new_status}',UPDATE_TS = getdate() Where ITEM_MASTER_ID in (Select ITEM_MASTER_ID From ITEM_STYLE_INFO Where ITEM_CD ='{item_cd}')"
     #print(queryString)
     cursor.execute(queryString)
     conn.commit()
     
     cursor.close()
     conn.close()  
     
def updateNewLaunchItemColorsStatus(item_cd,new_status):
     conn = connectToMSSQLServer()
     cursor = conn.cursor()
     queryString = f"Update MDB_ITEM_VARIANT Set MDB_ITEM_VARIANT.Status='{new_status}',UPDATE_TS = getdate() Where ITEM_MASTER_ID in (Select ITEM_MASTER_ID From ITEM_STYLE_INFO Where ITEM_CD ='{item_cd}')"
     cursor.execute(queryString)
     conn.commit()
     
     cursor.close()
     conn.close() 
     
def updateNewLaunchItemColorsStatusViaItemNo(item_nos,new_status):
     conn = connectToMSSQLServer()
     cursor = conn.cursor()
     queryString = f"Update MDB_ITEM_VARIANT Set MDB_ITEM_VARIANT.Status='{new_status}',UPDATE_TS = getdate() Where ITEM_NO in ({item_nos})"
     print(queryString)
     cursor.execute(queryString)
     conn.commit()
     
     cursor.close()
     conn.close()      
 
def updateNewItemUATStatus(item_cd,new_status):
     conn = connectToMSSQLServer()
     cursor = conn.cursor()
     queryString = f"update MDB_ITEM_FLD_VALUE set VALUE_INT = {new_status},UPDATE_TS = getdate() where ITEM_MASTER_ID in (Select ITEM_MASTER_ID From ITEM_STYLE_INFO Where ITEM_CD ='{item_cd}') and ITEM_FLD_ID = {constants.ITEM_FLD_ID_UAT_DISPLAY_ONLY}";
     cursor.execute(queryString)
     conn.commit()
     
     cursor.close()
     conn.close()  
      
def getItemStatus(item_cd): 
     conn = connectToMSSQLServer()
     cursor = conn.cursor() 
     queryString = f"Select Status From ITEM_STYLE_INFO Where ITEM_CD ='{item_cd}'" 
     cursor.execute(queryString)
     
     item_status = cursor.fetchone()

     return item_status.Status                       
        