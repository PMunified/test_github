import mongoDBManager as mongoDBHandler 
import constants  
import fileHandler
import os
import csv, sys

def generateDataRow(item,sku,keys_list):
          data_sku = []  
          data_sku.append(item['PRODUCT_NAME'])
          data_sku.append(item['product_type']) 
          data_sku.append(item['selling_method'])  
          data_sku.append(sku[keys_list[0]]['usd']['qty']) #Minimum order quantity
          data_sku.append(float(sku[keys_list[0]]['usd']['price'])*0.60) #USD unit wholesale price
          data_sku.append(sku[keys_list[0]]['usd']['price']) #USD unit retail price
          data_sku.append(";".join(item['blank_images'])) #Product image URLs
          data_sku.append(item['PRODUCT_DESC']) #Product description
          data_sku.append(item['weight']) #Item weight
          data_sku.append(item['weight_uom']) #Item weight UOM
          data_sku.append(item['length']) #Item length
          data_sku.append(item['width']) #Item width 
          data_sku.append(item['height']) #Item height
          data_sku.append(item['dimension_uom']) #Item dimensions
          data_sku.append(sku['color']) #colors
          data_sku.append(keys_list[0]) #SKU
          data_sku.append(sku[keys_list[0]]['cad']['qty']) #CAD retail price
          data_sku.append(float(sku[keys_list[0]]['cad']['price'])*0.60) #CAD unit wholesale price
          data_sku.append(sku[keys_list[0]]['cad']['price']) #CAD retail price 
          data_sku.append(sku['1']) #Inventory
          data_sku.append(sku['US1']) #Inventory
          return data_sku  
      
def outputCSVReport(file_name,data):
    # Open the file in write mode
    with open(file_name, mode='w', encoding='UTF-8',newline='') as file:
        writer = csv.writer(file)
    
    # Write each row of data to the file
        for row in data:
            writer.writerow(row)

    print(f"Data written to {file_name}")            

currentDir = os.path.realpath(os.path.dirname(__file__)) #Get current work folder
fh = fileHandler.classFileHandler(currentDir+"/faireItems.csv")
theList = fh.getLaunchItemList()
currentItemCD = ""
allItemCds = []
allValidSKUs = []
for x in theList:
   params = x.split('\t') 
   if (len(params)>1):
       if (params[0]!=''):
          allItemCds.append(params[0])
   allValidSKUs.append(params[1])       
#sys.exit(0)   
mongodbInstance = mongoDBHandler.mongoDBManager(constants.MONGODB_HOSTED_IP,constants.MONGODB_DATABASE_NAME)
'''
data = [
    ["Product name","Product type","Selling method","Minimum order quantity","USD unit wholesale price"
     ,"USD unit retail price","Product image URLs","Product description",
     "Item weight","Weight UOM","Item length","Item width","Item height","Item dimensions","Option (colours)","SKU",
     "Minimum order quantity (CAD)","CAD unit wholesale price","CAD retail price","inventory","inventory_us"]
]
'''
data = [["ITEM_CD","SKU","Image_URL"]]
items = allItemCds#['G1079','ST4143']
''' 
items_skus = {}
for item in theList:
    params = item.split('\t')
    items.append(params[0])
    items_skus[params[0]] = params[1]
'''   
#results = mongodbInstance.getListOfSupplierProducts(items) 
results = mongodbInstance.getMontageImageListOfSupplierProducts(items,allValidSKUs); 
print(results)
for x in results:
 data.append(x)
'''
allItems = results['item_list']
for item in allItems:
    item_code = item['PRODUCT_CODE']
    allSkus = items_skus[item_code]
    if (allSkus=='ALL'):
        skus = item['skus']        
        for sku in skus: 
          keys_list = list(sku.keys())
          data.append(generateDataRow(item,sku,keys_list))
    else:
        handledSkus = allSkus.split(",") 
        skus = item['skus'] 
        for sku in skus:
            keys_list = list(sku.keys())
            correctSku = False
            for showSku in handledSkus:
                if (keys_list[0].endswith(showSku.strip())):
                    correctSku = True
                    break
            if correctSku:
                data.append(generateDataRow(item,sku,keys_list))                         
'''
file_name = "OraFaireList.csv"
outputCSVReport(file_name,data)