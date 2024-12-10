class classFileHandler:
    className = "classFileHandler"
    def __init__(self,filePath):
        self.filePath = filePath
    
    def test():
        print("Test function")
        
    def test_item_code_change():
        print("Item code change.") 
        
    def update_item_to_mongoDB():
        print("Update item code to mongoDB")       
            
    def getLaunchItemList(self):
            #print(abc)
            itemList = list()
            myfile = open(self.filePath, "r")
            myline = myfile.readline()
            while myline:
             itemList.append(myline.replace('\n',""))
             myline = myfile.readline()
            myfile.close() 
            return itemList
                 