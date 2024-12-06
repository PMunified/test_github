import requests
import constants
finalURL = f"{constants.COSTING_UPDATE_URL}?user={constants.ACCESS_USER}&style="
# this way is used for http Get  request without params
def updateDataFromMDB(item_cd,new_status):
   reqURL = f"{finalURL}{item_cd}&status={new_status}" 
   print(reqURL)  
   response = requests.get(finalURL)
   status = response.reason
   if (status=='OK'):
      return True
   else:
      return False
# this way is used for http Get  request with params   
def updateDataFromMDBViaGet(item_cd,new_status):
    reqURL = constants.COSTING_UPDATE_URL
    payLoad = {'user':constants.ACCESS_USER,'style':item_cd,'status':new_status}
    response = requests.get(reqURL,params=payLoad)
    print(response.url)
    status = response.reason
    if (status=='OK'):
      return True
    else:
      return False    
      