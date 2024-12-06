class classFileHandler:
    className = "classFileHandler"
    def __init__(self,filePath):
        self.filePath = filePath
    
        
    def getLaunchItemList(self):
            #print(abc)
            itemList = list()
            myfile = open(self.filePath, "r")
            myline = myfile.readline()
            while myline:
             itemList.append(myline.replace('\n',""))
             myline = myfile.readline()
            myfile.close() 
            #Calling private method inside class
            #self.__privateMethod(abc)
            return itemList
    '''   
    def _protectedMethod(self,abc):
            #Calling private method inside class
            self.__privateMethod(abc)
            print(f"protected method:{self.className}{abc}")   
            
    def __privateMethod(self,abc):
            print(f"call private method:{abc}") 
            
    @classmethod
    def classMethod(cls,abc):
        cls.filePath = f"{cls.className}" 
        print(f"this is class method {abc}{cls.filePath}")
    
    @staticmethod
    def staticMethod(abc):
        print(f"this is static method:{abc}")   
    '''                 