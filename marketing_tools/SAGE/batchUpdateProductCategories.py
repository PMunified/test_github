import requests
import json
import fileHandler
import os

api_url = "https://web1.promoplace.com/ws/ws.dll/ConnectAPI"
headers = {
    "Content-Type": "application/json"    
}

def loadCategoriesUpdateList():
    currentDir = os.path.realpath(os.path.dirname(__file__)) 
    fh = fileHandler.classFileHandler(currentDir+"/categoryUpdate1.csv")
    itemList = fh.getLaunchItemList()
    allUpdates = {}
    for item in itemList:
        params = item.split(",")
        if (params[2]!=''):
            allUpdates[params[0]] = params[1]+";"+params[2]
        else:
            allUpdates[params[0]] = params[1]    
    return allUpdates

def getSAGECategories():
    product_data = {
                "serviceId":101,
                "apiVer":"110",
                "Auth": {
                        "AcctID":2681,
                        "key" : "4154fd4121a9c8f88c581fec3658cb8b"
                }
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(product_data))
    productCategories = {}
    # Check if the request was successful
    if response.status_code == 200:
        print("Product updated successfully!")
        jsonResponse = response.json()
        categories = jsonResponse['Categories']
        for category in categories:
          productCategories[category['Name']]=category['ID']
        #print(len(products))
    else:
        print(f"Failed to update product. Status code: {response.status_code}")
        print("Response:", response.text)
    #print(len(productCategories))
    return productCategories 

def getSAGEThemes():
    product_data = {
                "serviceId":102,
                "apiVer":"110",
                "Auth": {
                        "AcctID":2681,
                        "key" : "4154fd4121a9c8f88c581fec3658cb8b"
                }
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(product_data))
    productThemes = {}
    # Check if the request was successful
    if response.status_code == 200:
        print("Product updated successfully!")
        jsonResponse = response.json()
        print(jsonResponse)
        themes = jsonResponse['Themes']
        for theme in themes:
          productThemes[theme['Name']] = theme['ID']
        #print(len(products))
    else:
        print(f"Failed to update product. Status code: {response.status_code}")
        print("Response:", response.text)
    #print(len(productCategories))
    return productThemes       

def getProductIdPaires(sageNum:str):
    product_data = {
                "serviceId":108,
                "apiVer":"110",
                "Auth": {
                    "AcctID":2681,
                    "key" : "4154fd4121a9c8f88c581fec3658cb8b"
                    },
                "SAGENum":sageNum
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(product_data))
    productIdPaires = {}
    # Check if the request was successful
    if response.status_code == 200:
        print("Product updated successfully!")
        jsonResponse = response.json()
        products = jsonResponse['products']
        for product in products:
            productIdPaires[product['itemNum']]=product['productId']
        #print(len(products))
    else:
        print(f"Failed to update product. Status code: {response.status_code}")
        print("Response:", response.text)
    return productIdPaires

def generateProductsCategoriesUpdates(productIdPaires:dict,
                           productCategories:dict,productCategoriesUpdates:dict,
                           sageNum:str):
    categoriesUpdates = []
    products = list(productCategoriesUpdates.keys())
    for product in products:
        assignedCategories = productCategoriesUpdates[product]
        params = assignedCategories.split(";")
        update = {
                     "updateType":3,
                     "productId":productIdPaires[product],
                     "suppId":sageNum,
                     "itemNum":product,
                     "cat1Id":productCategories[params[0]],
                     "cat1Name":params[0]   
                }
        if len(params)>1:
           update['cat2Id'] = productCategories[params[1]]
           update['cat2Name'] = params[1]
        categoriesUpdates.append(update)    
    print(categoriesUpdates)        
    return categoriesUpdates
    

def updateProductsCategory(sageNum:str,
                           products:list):
    product_data = {
                "serviceId":109,
                "apiVer":"110",
                "Auth": {
                    "AcctID":2681,
                    "key" : "4154fd4121a9c8f88c581fec3658cb8b"
                    },
                "SAGENum":sageNum,
                "products":products
    }    
    response = requests.post(api_url, headers=headers, data=json.dumps(product_data))

    # Check if the request was successful
    if response.status_code == 200:
        print("Product updated successfully!")
        jsonResponse = response.json()
        print("Response:", jsonResponse)
    else:
        print(f"Failed to update product. Status code: {response.status_code}")
        print("Response:", response.text)
        
def deleteProduct(item_cds:list,sageNum:str,productIdPaires:dict):
    product_data = {
                "serviceId":109,
                "apiVer":"110",
                "Auth": {
                    "AcctID":2681,
                    "key" : "4154fd4121a9c8f88c581fec3658cb8b"
                    },
                "SAGENum":sageNum,
                "products":generateProductsDeleteList(productIdPaires,item_cds,sageNum)
    }    
    response = requests.post(api_url, headers=headers, data=json.dumps(product_data))

    # Check if the request was successful
    if response.status_code == 200:
        print("Product updated successfully [Delete]!")
        jsonResponse = response.json()
        print("Response:", jsonResponse)
    else:
        print(f"Failed to update product. Status code: {response.status_code}")
        print("Response:", response.text)  
         
def generateProductsDeleteList(productIdPaires:dict,item_cds:list,sageNum:str):
    deleteDataList = []
    for item_cd in item_cds:
        deleteData = {
               "updateType":3,
               "productId":productIdPaires[item_cd],
               "suppId":sageNum,
               "itemNum":item_cd,
               "delete":1,             
        }
        deleteDataList.append(deleteData)  
    return deleteDataList           
######################################################
# themes	Comma-separated list of themes	string	200
#
#
######################################################  
#allThemes = getSAGEThemes()  
''' update item categories which provided by SAGE            
productCategories = getSAGECategories()
categoriesUpdates = loadCategoriesUpdateList()
supplierIds = ["61086","65332"]   
for id in supplierIds: 
    print("Process Suppplier Id:"+id)    
    productIdPaires = getProductIdPaires(id)  
    updatedProducts = generateProductsCategoriesUpdates(productIdPaires,productCategories,categoriesUpdates,id)
    updateProductsCategory(id,updatedProducts)
''' 
# Delete items from SAGE
deleteList = ["GF899"]
supplierIds = ["61086","65332"]   
for id in supplierIds: 
    print("Process Suppplier Id:"+id)    
    productIdPaires = getProductIdPaires(id)  
    deleteProduct(deleteList,id,productIdPaires)