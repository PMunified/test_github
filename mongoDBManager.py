from pymongo import MongoClient
import json
import constants  

class mongoDBManager:
    def __init__(self,mongoDBHostIP,mongoDBName,HostPort='27017'):
        self.mongoDBHostIP = mongoDBHostIP
        self.mongoDBName = mongoDBName
        self.hostPort = HostPort
        self.mongoClient = self.__getClient()
        self.mydb = self.mongoClient[f"{self.mongoDBName}"]
    
    def __getClient(self):
        return MongoClient(f"mongodb://{self.mongoDBHostIP}:{self.hostPort}/")
    
    def getMontageImageListOfSupplierProducts(self,
                                  itemList:list,
                                  validSKUs:list,
                                  tableName:str = "products"):
        mycol = self.mydb[f"{tableName}"] 
        filter = {}
        filter['ITEM_CD'] = {"$in":itemList}
        projections = {'_id':0,
                       'ITEM_CD':1,
                       "VARIANTS":1}
        results =  mycol.find(filter,projections) 
        if (results != None):  
            itemList = []  
            for result in results:
                if ('VARIANTS' in result):
                    Variants = result['VARIANTS'] 
                    for sku in Variants:
                        if (sku in validSKUs):
                            if ('DOCUMENT' in Variants[sku]):
                                image = [result['ITEM_CD'],sku]
                                image.append(constants.SPECTOR_ITEM_IMAGE_URL_BASE+Variants[sku]['DOCUMENT']['name'])
                                itemList.append(image) 
                            else:
                                image = [result['ITEM_CD'],sku,"No image"]  
                                itemList.append(image)          
            return itemList
        else:
            return []           
    
    def getListOfSupplierProducts(self,
                                  itemList:list,
                                  tableName:str = "products"):
        mycol = self.mydb[f"{tableName}"] 
        filter = {}
        filter['ITEM_CD'] = {"$in":itemList}
        projections = {'_id':0,
                       'ITEM_CD':1,'WEB_PROD_NAME':1,"WEB_PROD_DESC_US":1, 
                       "WEIGHT":1,"WEIGHT_W_PKG":1,"WEIGHT_UOM_ID":1,                      
                       "SIZE_X":1,"SIZE_Y":1,"SIZE_Z":1,"SIZE_UOM_ID":1,                       
                       "WEIGHT":1,"WEIGHT_UOM_ID":1,
                       'VARIANTS':1,
                       'DOCUMENTS':1,
                       "DOCUMENTS":1}
        results =  mycol.find(filter,projections) 
        if (results != None):  
            itemList = []                         
            for result in results:
               item = {}
               item['PRODUCT_CODE'] = result['ITEM_CD'] 
               item['PRODUCT_NAME'] = result['WEB_PROD_NAME']
               item['PRODUCT_DESC'] = result['WEB_PROD_DESC_US']
               item['product_type'] = "TBD"
               item['selling_method'] = "By item"
               item['length'] = result['SIZE_X']
               item['width'] = result['SIZE_Y']
               item['height'] = result['SIZE_Z']
               item['dimension_uom'] = "inch"
               item['weight'] = result['WEIGHT']
               item['weight_uom'] = result['WEIGHT_UOM_ID']
               item_blank_images = []
               if ('DOCUMENTS' in result):
                   documents = result['DOCUMENTS']
                   for doc in documents:
                       if (doc=='BLANKS'):
                           blankdocs = documents[doc]
                           for image in blankdocs:
                               item_blank_images.append(constants.SPECTOR_ITEM_IMAGE_URL_BASE+image['name']) 
                           break
               item['blank_images'] = item_blank_images
               item_varinats = []  
               items_colors = []
               if ('VARIANTS' in result):
                   allVariants = result['VARIANTS']
                   for sku in allVariants:
                       price_usd = {} 
                       items_colors.append(allVariants[sku]['COLOR_NAME'])
                       if ('USD' in allVariants[sku]['PRICES']['DOMESTIC']):
                            qty=  allVariants[sku]['PRICES']['DOMESTIC']['USD']['minimum_qty_1'] 
                            price = allVariants[sku]['PRICES']['DOMESTIC']['USD']['minimum_prc_1'] 
                            price_usd['qty'] = qty
                            price_usd['price'] = price 
                       price_cad = {} 
                       if ('CAD' in allVariants[sku]['PRICES']['DOMESTIC']):                              
                            qty=  allVariants[sku]['PRICES']['DOMESTIC']['CAD']['minimum_qty_1'] 
                            price = allVariants[sku]['PRICES']['DOMESTIC']['CAD']['minimum_prc_1'] 
                            price_cad['qty'] = qty
                            price_cad['price'] = price 
                       inventory_ca = 0
                       inventory_us = 0
                       if ('INVENTORY' in allVariants[sku]):
                           inventory = allVariants[sku]['INVENTORY']
                           if ("1" in inventory):
                                inventory_ca =  inventory['1']['qtyAvailable']  
                           if ("US1" in inventory):
                                inventory_us = inventory['US1']['qtyAvailable']                            
                       item_varinats.append({sku:{"usd":price_usd,"cad":price_cad},"color":allVariants[sku]['COLOR_NAME'],"1":inventory_ca,"US1":inventory_us}) 
               item['skus'] = item_varinats 
               item['colors'] = items_colors         
               itemList.append(item)   
            return_list = {"count":len(itemList),"item_list":itemList}   
            return return_list   
        else:
            return [] 
        
    def getQuantityAndPriceOfProducts(self,
                                  itemList:list,
                                  currencyCode:str,
                                  tableName:str = "products"):
        mycol = self.mydb[f"{tableName}"] 
        filter = {}
        filter['ITEM_CD'] = {"$in":itemList}
        projections = {'_id':0,
                       'ITEM_CD':1, 
                       'VARIANTS':1}
        results =  mycol.find(filter,projections) 
        if (results != None):  
            items = {}                        
            for result in results:               
               allQtyPlusPricesOfItem = []
               if ('VARIANTS' in result):
                   allVariants = result['VARIANTS']                  
                   for sku in allVariants:
                       status = allVariants[sku]['ColorStatus']
                       if (status in ['lau','wql','dis','red']):
                           if ('PRICES' in allVariants[sku]):
                            if (currencyCode in allVariants[sku]['PRICES']['DOMESTIC']):
                                qty = []
                                price = []
                                for index in range(1,6):
                                    if (status=='wql'):
                                        qty.append(round(float(allVariants[sku]['PRICES']['DOMESTIC'][currencyCode]['WQL']['minimum_qty_'+str(index)]))) 
                                        price.append(format(float(allVariants[sku]['PRICES']['DOMESTIC'][currencyCode]['WQL']['minimum_prc_'+str(index)]),".2f"))                                         
                                    else:    
                                        qty.append(round(float(allVariants[sku]['PRICES']['DOMESTIC'][currencyCode]['minimum_qty_'+str(index)]))) 
                                        price.append(format(float(allVariants[sku]['PRICES']['DOMESTIC'][currencyCode]['minimum_prc_'+str(index)]),".2f")) 
                                qty.append(0)
                                price.append('0.00')
                                tmp = {'Qty':qty,'Prices':price}
                                if (tmp not in allQtyPlusPricesOfItem):
                                    allQtyPlusPricesOfItem.append({'Qty':qty,'Prices':price})
                            items[result['ITEM_CD']] = allQtyPlusPricesOfItem            
            return items  
        else:
            return {}             