from pymongo import MongoClient
import json 


class mongoDBManager:
    def __init__(self,mongoDBHostIP,mongoDBName,HostPort='27017'):
        self.mongoDBHostIP = mongoDBHostIP
        self.mongoDBName = mongoDBName
        self.hostPort = HostPort
        self.mongoClient = self.__getClient()
        self.mydb = self.mongoClient[f"{self.mongoDBName}"]
    
    def __getClient(self):
        return MongoClient(f"mongodb://{self.mongoDBHostIP}:{self.hostPort}/")
    
    def getAllNonORAItemsWithORASpecification(self,
                          tableName:str="products"):
        mycol = self.mydb[f"{tableName}"] 
        filter = {}
        filter['PROD_CAT'] = {"$ne":"ORA"}
        filter['Status'] = {"$in":['lau','dis','wql']}
        filter['UAT_DISPLAY_ONLY'] = "0"
        filter['NOT_FOR_INDIVIDUAL_SALE'] = "0"
        results =  mycol.find(filter) 
        count = 0
        if (results != None):
            for item in results:
                if "ORA_Specification" in item:
                   oraSpecification = item['ORA_Specification']
                   if len(oraSpecification)>0:
                      count = count + 1
                      print(item['ITEM_CD'])
        print(count)        
        