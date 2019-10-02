import pyodbc 



class SQLStore():
    def __init__(self):
        super(SQLStore,self).__init__()
        
        self.connection = "Driver={SQL Server};Server=BRMN2012\SQLEXPRESS;Database=sahibinden;UID=shb;PWD=tyfn34--"


    def createBrands(self,brands):
        
        try:
            conn = pyodbc.connect(self.connection)        
            cursor = conn.cursor()
            for i in brands:
                name = i["Name"]
                uri = i["Url"]
                cursor.execute('insert into  brands (Name,Url) values (?,?)', (name,uri))
                
            conn.commit()
            print("SUCCESS! --->" + "Markalar başarı ile aktarıldı.")
        except:
            print("ERROR! --->" + "Markalar Aktarılırken hata oluştu!")
            
    def getBrands(self):
        conn = pyodbc.connect(self.connection)        
        cursor = conn.cursor()
        cursor.execute("select * from brands")
        result = cursor.fetchall()
        return result

    def getModels(self):
        conn = pyodbc.connect(self.connection)        
        cursor = conn.cursor()
        cursor.execute("select * from models")
        result = cursor.fetchall()
        return result

    def getVersions(self):
        conn = pyodbc.connect(self.connection)        
        cursor = conn.cursor()
        cursor.execute("select  * from versions where IsQuery = 0")
        result = cursor.fetchall()
        return result
    
    def getVersionById(self,version_id):
        conn = pyodbc.connect(self.connection)        
        cursor = conn.cursor()
        cursor.execute("select * from versions where Id = ?",(version_id))
        result = cursor.fetchall()
        return result
    
    def createModels(self,models):
        try:
            conn = pyodbc.connect(self.connection)        
            cursor = conn.cursor()
            for i in models:
                name = i["Name"]
                uri = i["Url"]
                brand_id = i["BrandId"]
                cursor.execute('insert into  models (Name,Url,BrandId) values (?,?,?)', (name,uri,brand_id))
                
            conn.commit()
            print("SUCCESS! --->" + "Modeller başarı ile aktarıldı.")
        except:
            print("ERROR! --->" +  " BrandID = " +  i["BrandId"] + " ---- > Modeller Aktarılırken hata oluştu!")
            
            
    def createVersions(self,versions):
        try:
            conn = pyodbc.connect(self.connection)        
            cursor = conn.cursor()
            for i in versions:
                name = i["Name"]
                uri = i["Url"]
                model_id = i["ModelId"]
                cursor.execute('insert into  versions (Name,Url,ModelId) values (?,?,?)', (name,uri,model_id))
                
            conn.commit()
            print("SUCCESS! --->" + "Versiyonlar başarı ile aktarıldı.")
        except:
            print("ERROR! --->" +  " ModelId = " +  i["ModelId"] + " ---- > Versiyonlar Aktarılırken hata oluştu!")
            

    def createSubVersions(self,sub_versions):
        try:
            conn = pyodbc.connect(self.connection)        
            cursor = conn.cursor()
            for i in sub_versions:
                name = i["Name"]
                uri = i["Url"]
                version_id = i["VersionId"]
                cursor.execute('insert into subversions (Name,Url,VersionId,IsQuery) values (?,?,?,?)', (name,uri,version_id,False))
            
            cursor.execute('update versions set IsQuery = 1 where Id = ?', (version_id))
            conn.commit()
            print("SUCCESS! --->" + "Alt versiyonlar başarı ile aktarıldı.")
        except:
            print("ERROR! --->" +  " VersionId = " +  i["VersionId"] + " ---- > Alt versiyonlar Aktarılırken hata oluştu!")