import requests
import json
#import fileHandler
#import os

api_login_url = "https://productservice.asicentral.com/api/v5/login"
api_delete_product_url = "https://productservice.asicentral.com/api/v5/products/"


def getAccessToken(api_login_url:str,_paramters:dict):
    paramters = _paramters
    headers = {
        "accept": "application/json",
        "content-type": "application/json"    
    }    
    
    response = requests.post(api_login_url, headers=headers, data=json.dumps(paramters))
    if response.status_code == 200:
        print("Get Access Token successfully!")
        jsonResponse = response.json()
        return jsonResponse['AccessToken']
    else:
        print(f"Failed to get access token. Status code: {response.status_code}")
        print("Response:", response.text)
    #print(len(productCategories))
        return "" 
def deleteProductFromESP(api_delete_product_url:str,accessToken:str,item_cd:str):
    headers = {
        "accept": "application/json",
        "cache-control":"no-cache",
        "authtoken":accessToken,
        "content-type": "application/json"    
    }     
    response = requests.delete(api_delete_product_url+item_cd, headers=headers)#, data=json.dumps(paramters))
    if response.status_code == 200:
        print("Delete product successfully!")
    else:
        print(f"Failed to delete product. Status code: {response.status_code}")
        print("Response:", response.text) 
         
def printInfo():
    print("Welcome to printinfo function.")
    print("welcome to here.")
        
             
currencies = ["CAD","USD"]
login_secrets = {
    "CAD": {
        "ASI":"88631",
        "Username":"SpectorCan",
        "Password":"zaq1xsw2cde3vfr4"
    },
    "USD":{
        "ASI":"88660",
        "Username":"Stevent@spectorandco.com",
        "Password":"password2"
    }
}

deleteList = ["GF899"]
for currency in currencies:
    accessToken = getAccessToken(api_login_url,login_secrets[currency])
    for item in deleteList:    
        deleteProductFromESP(api_delete_product_url,accessToken,item)
