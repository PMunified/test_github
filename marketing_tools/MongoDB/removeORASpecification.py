import cleanORASpecification as backendDB
MONGODB_HOSTED_IP = "104.207.251.33"
MONGODB_DATABASE_NAME = "ashburyDB"
instance = backendDB.mongoDBManager(MONGODB_HOSTED_IP,MONGODB_DATABASE_NAME)
instance.getAllNonORAItemsWithORASpecification()