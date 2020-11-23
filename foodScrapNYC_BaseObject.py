#Import Declarations
import pymysql, csv, time

#Reading Destination File for SQL Processing
foodScrapRatingCSVFile = open('generatedFiles/LatLongLocation.csv', 'r')
readFoodScrapRatingDetailsFileCSV = foodScrapRatingCSVFile.read()
csvHeader = readFoodScrapRatingDetailsFileCSV.split("\n")[0]
tableCols = csvHeader.split(",")
tableName = 'manoha_ia626_foodscrapdropofflocations'

class baseObject:
    #Table Declaration & Initial SQL Processing Calls
    def setupObject(self,tableName):
        self.data = []
        self.tempdata = {}
        self.tableName = tableName
        self.fn1 = []
        self.errList = []
        self.conn = None
        self.pk = ''
        self.rating = 'rating'
        self.creatTable()
        self.getFields()
        self.insertData()

    #DB Config Import and Configurations
    def connect(self):
        import config
        self.conn = pymysql.connect(host=config.DB['host'],port=config.DB['port'],user=config.DB['user'],password=config.DB['password'],db=config.DB['db'],autocommit=True)
    
    #Create Table Function Call - Assigning Datatypes
    def creatTable(self):
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #Dropping Table If already exists
        cur.execute("DROP TABLE IF EXISTS `manoha_ia626_foodscrapdropofflocations`;")

        #Create Table Script - Convert Fieldnames to Lowercase and Strip
        sql = '''CREATE TABLE IF NOT EXISTS `'''+tableName+'''` (
          `fsID` int(5) NOT NULL AUTO_INCREMENT,
        '''
        buf = ''

        for fieldName in tableCols:
            nfn = fieldName.replace(' ','').lower().strip()
            #Based on condition assigning different datatypes for fieldnames
            if 'latitude' in nfn or 'longitude' in nfn:
                buf += '`' + nfn + '` DECIMAL(18,15) NOT NULL, \n'
            elif 'population' in nfn:
                buf += '`' + nfn + '` int(10) NOT NULL, \n'
            elif 'rating' in nfn:
                buf += '`' + nfn + '` float(3,1) NOT NULL, \n'
            else:
                buf += '`' + nfn + '` varchar(200) NOT NULL, \n'

        sql = sql + buf + ''' PRIMARY KEY (`fsID`)
        ) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;'''

        cur.execute(sql)  

    #Reading Table Fieldnames From SQL 
    def getFields(self):
        sql = 'DESCRIBE `' + self.tableName +'`;'
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        self.fn1 = []
        for row in cur:
            self.fn1.append(row['Field'])
            if row['Extra'] == 'auto_increment' and row['Key'] == 'PRI':
                self.pk = row['Field']
            if type(row['Field']) == float:
                self.rating = row['Field']
                print(self.rating)

    #Reading Output File Row by Row and Inserting into SQL Table
    def insertData(self):
        tokens = []
        i = 0
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = '''INSERT INTO `'''+tableName+'''` (`borough`,`food_scrap_drop_off_site_name`,`latitude`,
                `longitude`,`location`,`ntaname`,`serviced_by`,`population`,`placeid`,`rating`)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''' 

        #Reading LatLongLocation.csv for inserting CSV rows into PHPMyAdmin
        with open('generatedFiles/LatLongLocation.csv') as f:
            data = [{k: str(v) for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]

        blocksizes = [100]
        for bs in blocksizes:
            start2 = time.time()
            for fsRow in data:  

                #Getting actual fieldnames from CSV and appending to tokens for SQL injection
                tokens.append((fsRow["Borough"],fsRow["Food_Scrap_Drop_Off_Site_Name"],fsRow["Latitude"],
                fsRow["Longitude"],fsRow["Location"],fsRow["NTAName"],
                fsRow["Serviced_by"],fsRow["Population"],fsRow["PlaceID"],fsRow["Rating"]))

            if i % bs == 0 and i != 0:
                bstart = time.time()
                cur.executemany(sql,tokens)
                self.conn.commit()
                 #Token is emptied for each block iteration to populate with new token entries
                tokens = []
            i+=1
            print ("For the Block Size: " + str(bs) + "\nTotal Time Taken for Execution: " + str(time.time() - start2))
           
            #The below if condition is to group token which are out of the modulus of blocksize
            if len(tokens) > 0:
                cur.executemany(sql,tokens)
                self.conn.commit()
    
    #Reading SQL Data For Neighborhood Population Details
    def getByNTAName(self):
        sql = 'SELECT DISTINCT(ntaname), borough, population FROM `' + self.tableName +'` GROUP BY ntaname;' 
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        self.data = []
        for row in cur:
            self.data.append(row)    

    #Reading SQL Data For Food Scrap Drop Off Location Details
    def getByFoodScrapDropOffLocation(self):
        sql = 'SELECT DISTINCT(ntaname), borough, food_scrap_drop_off_site_name, location, serviced_by FROM `' + self.tableName +'` GROUP BY serviced_by;' 
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        self.data = []
        for row in cur:
            self.data.append(row)        

    #Reading SQL Data For Food Scrap Drop Off Location Based on Rating Details
    def getByRating(self,rating):
        sql = 'SELECT DISTINCT(food_scrap_drop_off_site_name), borough, location, ntaname, serviced_by, rating FROM `' + self.tableName +'` WHERE `'+self.rating+'` = %s;' 
        tokens = (rating)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql,tokens)
        self.data = []
        for row in cur: 
            self.data.append(row)

    #Reading SQL Data For Food Scrap Drop Off Location to Fetch All Rating Details
    def getAllRating(self):
        sql = 'SELECT DISTINCT(rating) FROM `' + self.tableName +'` ORDER BY rating;'
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        self.data = []
        for row in cur: 
            self.data.append(row)
    
