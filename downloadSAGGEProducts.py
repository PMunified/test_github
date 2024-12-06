import mongoDBManager as mongoDBHandler 
import constants  
import requests
import json
import fileHandler
import os

currentDir = os.path.realpath(os.path.dirname(__file__)) #Get current work folder
fh = fileHandler.classFileHandler(currentDir+"/pricesUPgradeList0602.csv")
theList = fh.getLaunchItemList()
################### SAGE ######################################################
url = "https://web1.promoplace.com/ws/ws.dll/ConnectAPI"
service_code = '108'
sage_num = '61086'
 

headers = {
    'Content-Type': 'application/json'
}
################### SAGE ######################################################
############################## ASI/ESP ########################################
headers_esp = {
    'Content-Type': 'application/json',
    'accept': 'application/json', 
    'cache-control': 'no-cache'      
}

def getAccessToken(asi_number:str,
                   asi_username:str,
                   asi_password:str):
    req_url = "https://productservice.asicentral.com/api/v5/login"
    payloads = {
     'Asi': asi_number,
     'Username': asi_username,
     'Password' : asi_password  
    }
    accessToken = ""
    response = requests.post(req_url, headers=headers_esp, json=payloads)  
    if (response.status_code==200):
        try:
            response_json_obj = json.loads(response.text)
            accessToken = response_json_obj['AccessToken']
            #print(response_json_obj)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")    
    else:
        print("Could not get access token") 
    return accessToken       

def getProductsInfoFromESP(accessToken:str):
    req_url = "https://productservice.asicentral.com/api/v5/products/"
    headers_esp_p = headers_esp
    headers_esp_p['authtoken'] = accessToken
    count = 0
    response = requests.get(req_url, headers=headers_esp)  
    if (response.status_code==200):
        try:
            response_json_obj = json.loads(response.text)
            allProducts = response_json_obj['Products']
            for product in allProducts:
                print(product['ExternalProductId'])
                print(product['LastUpdateDateUtc'])
                print(product['ProductStatus'])
                count = count + 1 
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")    
    else:
        print(response.reason) 
    print("======>"+str(count))        
    return ""

def getProductDetailsInfoFromESP(accessToken:str,ExternalProductId:str):
    req_url = "https://productservice.asicentral.com/api/v5/products/"+ExternalProductId
    headers_esp_p = headers_esp
    headers_esp_p['authtoken'] = accessToken
    Qty = []
    Prices = []
    itemPriceInfo = {}
    response = requests.get(req_url, headers=headers_esp)  
    if (response.status_code==200):
        try:
            response_json_obj = json.loads(response.text)
            allPrices = response_json_obj['PriceGrids']
            for price in allPrices:
                if (price['IsBasePrice']):
                    listOfPrices = price['Prices']
                    for x in listOfPrices:
                        Qty.append(x['Qty'])
                        Prices.append(x['ListPrice'])
                    Qty.append(0)
                    Prices.append('0.00') 
                    itemPriceInfo['Qty'] = Qty
                    itemPriceInfo['Prices'] = Prices  
                    break
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")    
    else:
        print(response.reason) 
       
    print(itemPriceInfo)
    return itemPriceInfo
############################## ASI/ESP #############################################
############################## SAGE    #############################################
def getAllProductQtyAndPricesFromSAGE(url:str,
                                      headers:dict,
                                      service_code:str,
                                      sage_num:str):  
    payloads = {
                "serviceId":service_code,
                "apiVer":"110",
                "Auth": {
                    "AcctID":2681,
                    "key" : "4154fd4121a9c8f88c581fec3658cb8b"
                    },
                "SAGENum":sage_num
        }     
    response = requests.post(url, headers=headers, json=payloads)  
    allProductsPriceQtyArray = {}
    if (response.status_code==200):
        allProductsText = response.text
        try:
            json_obj = json.loads(allProductsText)
            allProducts = json_obj['products']
            for product in allProducts:
                if product['itemNum']=='DW301':
                    print(json.dumps(product))
                tmp =[]
                for index in range(0,6):
                    tmp.append(format(product['prices'][index],".2f"))
                allProductsPriceQtyArray[product['itemNum']] = {'Qty':product['quantities'],'Prices':tmp} 
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")     
    else:
        print(f'Reset failed with status code: {response.status_code}')
        print(f'Response: {response.text}')
    return allProductsPriceQtyArray     

############################################
###
###  Get Access token from ESP
###
############################################ 
#accessToken = getAccessToken('88660','Stevent@spectorandco.com','password2')
#getProductsInfoFromESP(accessToken)   #Get List of products info
#getProductDetailsInfoFromESP(accessToken,'G3111') #Get Product details info from ESP
#sys.exit(0)
############################## Valid price and Quantity from SAGE with MongoDB #################
sageItems = getAllProductQtyAndPricesFromSAGE(url,headers,'108','61086')  # USA-61086 #CAD:65332
#sageItems = getAllProductQtyAndPricesFromSAGE(url,headers,'108','65332') 
mongodbInstance = mongoDBHandler.mongoDBManager(constants.MONGODB_HOSTED_IP,constants.MONGODB_DATABASE_NAME)
testItems = theList #['ST4143','ST4340','I116','GF741']
#mongDBQtyAndprices = mongodbInstance.getQuantityAndPriceOfProducts(testItems,'USD')
mongDBQtyAndprices = mongodbInstance.getQuantityAndPriceOfProducts(testItems,'CAD')
#print(mongDBQtyAndprices)
#sys.exit(0)

count = 0
for item in testItems:
    if (item in sageItems):
        sagedict = sageItems[item]
        mongdBArray = mongDBQtyAndprices[item]
        if (sagedict in mongdBArray):
            #print("item["+item+"] is same")
            count = count + 1
        else:
            print(sagedict)
            print(mongdBArray)
            print("item["+item+"] is different") 
            count = count + 1   
print("==========================>")            
print(count)
############################## Valid price and Quantity from SAGE with MongoDB #################
############################## Valid price and Quantity from ASI/ESP with MongoDB #################
############################## Valid price and Quantity from ASI/ESP with MongoDB #################
