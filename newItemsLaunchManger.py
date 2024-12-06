import MSSQLServerModule
import constants
import webServiceAccess
import fileHandler
import os

currentDir = os.path.realpath(os.path.dirname(__file__)) #Get current work folder
fh = fileHandler.classFileHandler(currentDir+"/itemList.csv") #itemList.csv -- for new item
                                                              #BBList.csv -- for abandoned items, No need to run 
theList = fh.getLaunchItemList()
for item in theList: #item_cd:item_no
    if (item.rfind(":")>-1): # change status of item sku 
        item = item.strip()
        theList = item.split(":")
        print(theList[0])         
        item_status = MSSQLServerModule.getItemStatus(theList[0])
        MSSQLServerModule.updateNewLaunchItemColorsStatusViaItemNo(theList[1],constants.ITEM_STATUS_LAUNCH)
        #MSSQLServerModule.updateNewLaunchItemColorsStatusViaItemNo(theList[1],constants.ITEM_STATUS_ACTIVE)
        if (webServiceAccess.updateDataFromMDBViaGet(theList[0],item_status)):
            print("SKU Update is OK")
        else:
            print("SKU Update is failure")                      
        #print(theList[1])
    else: # change whole item status include all skus
        print(item)
        item = item.strip()
        MSSQLServerModule.updateNewLaunchItemStatus(item,constants.ITEM_STATUS_LAUNCH)
        MSSQLServerModule.updateNewLaunchItemColorsStatus(item,constants.ITEM_STATUS_LAUNCH)
        MSSQLServerModule.updateNewItemUATStatus(item,constants.UAT_DISPLAY_ONLY_YES)   
        #MSSQLServerModule.updateNewItemUATStatus(item,constants.UAT_DISPLAY_ONLY_NO)      
        if (webServiceAccess.updateDataFromMDBViaGet(item.strip(),constants.ITEM_STATUS_LAUNCH)):
            print("Item Update is OK")
        else:
            print("Item Update is failure")                  