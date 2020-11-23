# NYCFoodScrapingProject
 
 # IA 626: Big Data Processing & Cloud Services - Final Project Documentation

## Project Title: 

#### Big Data Inspection - NYC Food Scrap Drop Off Location Analysis
 
## Project Description:

The main purpose of this project is to analyze the dataset which contains information about the food scrap drop off location in NYC and perform various operations to understand the data. 

## Data Approach:

The below approach is followed for building this project,

Data Extraction : foodScrapNYC.py
Data Transformation : foodScrapNYC_SQL.py
Data Loading: foodScrapNYC_BaseObject.py

UI Application: foodScrapNYC_Main.py

The data flow used is depicted in the below flow diagram,

![GitHub Logo](/images/Flow_diagram.png)

## DataSet Used:

I have collected the data from NYC open data source repository. The column name, its description and datatype length are mentioned in below table.

| Column Name  | Description Type | DataType With Length |
| ----- | ------------- | ------------ |
| Borough | NYC Borough where vendor is located. New York City’s boroughs are five county-level administrative divisions, with each one also being a state county. | VARCHAR(50) |
| CouncilDist | NYC Council District Number. There are 51 Council districts throughout the five boroughs and is one is represented by an elected Council Member. | INT(10) |
| Food_Scrap_Drop_Off_Site_Name	| Name of food scrap drop-off location | VARCHAR(550) |
| Hours_from | Latest hour when food scraps can be dropped off. | VARCHAR(50) |
| Hours_to | Earliest hour when food scraps can be dropped off. | VARCHAR(50) |
| Latitude | Latitude of food scrap drop-off location for mapping purposes. | DECIMAL(9,6) | 
| Location | Street address or cross streets associated with food scrap drop-off location | VARCHAR(550) |
| Longitude	| Longitude of food scrap drop-off location for mapping purposes. | DECIMAL(9,6) | 
| NTAName | Neighborhood Tabulation Area Name. Neighborhood Tabulation Areas are small area boundaries that were initially created by the Department of City Planning for small area population projections. However, NTAs are now being used to present data from the Decennial Census and American Community Survey. | VARCHAR(550) |
| Notes	| Additional site notes | VARCHAR(550) |
| ObjectId | Id for Foodscraping | INT(10) |
| Operation_Day	| Days of the week when food scraps can be dropped off. | VARCHAR(50) |
| Open_Months | Months when food scraps can be dropped off at the location. | VARCHAR(50) |
| Serviced_by | Name of the organization that services the food scraps that are dropped off. | VARCHAR(550) |
| Website | Website associated with food scrap drop-off location. | VARCHAR(550) |
| boroCD | Borough and Community District which is represented by a single-digit borough number followed by two-digit borough community district number. | INT(10) |
| ct2010 | Census Tract (CT2010). The 2010 census tract in which the tax lot is located. | INT(10) |
| point	| Point | VARCHAR(50) |
| zip_code | Seven digit zip code of vendor | INT(10) |

## ETL Process:

### STEP-1: Data Extraction 

I have taken two datasets and two API's for my project analysis. The first dataset contains the food scrap drop off location site details for NYC boroughs. The second dataset contains the population details for NYC boroughs. The two google API's are considered for getting the rating details for food scrap drop off site location. 

For the ETL process, my first step was to merge the two CSV datasets. I merged the population dataset and food scrap drop off location dataset with the common factor which is NTAName (Neighborhood Name) using Python Pandas library.

    #Merging CSV File of Two Datasets (FoodScrapDropOffLocation & NTANeighborhood Population Details)
    df1 = pd.read_csv("datasets/Food_Scrap_Drop-Off_Locations_in_NYC.csv")
    df2 = pd.read_csv("datasets/New_York_City_Population_By_Neighborhood_Tabulation_Areas.csv")
    merged = pd.merge(df1,df2, on="NTAName").fillna("")
    merged.to_csv("generatedFiles/FoodScrap_Population_NTAName_Merge.csv", index=False)

Then, I extracted the ratings details for the food scrap drop off location using google APIs. The google places API requires placeid as parameter which was extracted from google geocoding API first, then the placeid was passed to places API for extracting ratings details. 

#### Google Geocoding API

    https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=YOUR_API_KEY

#### Google Places API

    https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name,rating,formatted_phone_number&key=YOUR_API_KEY

### STEP-2: Data Transformation

#### Generating JSON Files to Store the API Call Results

Since the API calls consumes time for each network call, I saved the API call results in JSON files for further processing. This is the one time call for fetching API results. The further processings are done with the generated JSON files for manipulations. This approach saved API Network call time and enhanced the execution rate.

The extracted data is then transformed into JSON file for processing.

    #Passing Latitude and Longitude Values One by One to Google API (GeoLocation API) to Fetch the Place ID 
    placeIDURL = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+row[5]+","+row[7]+"&result_type=establishment&key=AIzaSyCbhlpZo2bjxG_aIJT9XrZ-bMwnUOm0YC4"
    req1 = requests.get(placeIDURL)
    placeIDData = json.loads(req1.text)
    #Extracting the Exact PlaceID Value From JSON
    try:
        placeID = placeIDData['results'][0]['place_id']
    except IndexError:
        placeID =  "NA"
        pass
    #Writing the Extracted API PlaceID Results to JSON File
    latlongFile = open('generatedFiles/latlong/latlong_'+row[5]+'_'+row[7]+'.json','w')
    latlongFile.write('')
    latlongFile.write(req1.text)
    latlongFile.close()
    #Passing Extracted PlaceID Value From GeoLocation API One by One to Google API (Place Search API) to Fetch the Rating Details
    ratingURL = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+placeID+"&key=AIzaSyCbhlpZo2bjxG_aIJT9XrZ-bMwnUOm0YC4"
    req2 = requests.get(ratingURL)
    ratingData = json.loads(req2.text)
    #Extracting the Exact Rating Value From JSON
    try:
        rating = ratingData['result']['rating']
    except KeyError:
        rating =  0
        pass
    #Writing the Extracted API Rating Results to JSON File
    ratingFile = open('generatedFiles/rating/rating_'+placeID+'.json','w')
    ratingFile.write('')
    ratingFile.write(req2.text)
    ratingFile.close()

### STEP-3: Data Loading

After the data tranformation, I used the generated JSON file to read the required rating details to create destination/output CSV file.

    #Accessing JSON Files One by One Based on Latitude and Longitude Values
    latlongFileRead = open('generatedFiles/latlong/latlong_'+latKey+'_'+latLong[latKey]+'.json','r')
    latLongData = json.loads(latlongFileRead.read())
    #Extracting the Exact PlaceID Value From JSON
    try:
        placeID = latLongData['results'][0]['place_id']
    except IndexError:
        placeID =  "NA"
        pass
    latlongFileRead.close()
    #Accessing JSON Files One by One Based on PlaceID Values
    ratingFileRead = open('generatedFiles/rating/rating_'+placeID+'.json','r')
    ratingData = json.loads(ratingFileRead.read())
    #Extracting the Exact Rating Value From JSON
    try:
        rating = ratingData['result']['rating']
    except KeyError:
        rating =  0
        pass
    ratingFileRead.close()
    
    #Write To CSV File
    writer.writerow([row[0],row[2],row[5],row[7],row[6],row[8],row[13],populationConvert,placeID,rating])

Then, with the output CSV file, the data is read and loaded into SQL database.

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

The final destination table after processing is entered into the SQL. The column name, its description and datatype length are mentioned in below table.

| Column Name  | Description Type | DataType With Length |
| ----- | ------------- | ------------ |
| fsID | Food Scrap Drop Off Location Sequence ID | INT(5) |
| borough | NYC Borough where vendor is located. New York City’s boroughs are five county-level administrative divisions, with each one also being a state county. | VARCHAR(200) |
| food_scrap_drop_off_site_name	| Name of food scrap drop-off location | VARCHAR(200) |
| latitude | Latitude of food scrap drop-off location for mapping purposes. | DECIMAL(18,15) | 
| longitude	| Longitude of food scrap drop-off location for mapping purposes. | DECIMAL(18,15) | 
| location | Street address or cross streets associated with food scrap drop-off location | VARCHAR(550) |
| ntaname | Neighborhood Tabulation Area Name. Neighborhood Tabulation Areas are small area boundaries that were initially created by the Department of City Planning for small area population projections. However, NTAs are now being used to present data from the Decennial Census and American Community Survey. | VARCHAR(200) |
| serviced_by | Name of the organization that services the food scraps that are dropped off. | VARCHAR(200) |
| population | Population of NYC Borough Neighborhood | INT(10) |
| placeid | PlaceID for Location Extracted from API | VARCHAR(200) |
| rating | Rating for the Neighborhood Food Scrap Drop Off Site Location | FLOAT(3,1) |

## Analysis/Filtering:

### Data Visualization Analysis Using Tableau:

The main target of this project is to analyse the below questions for NYC food scrap dataset.

### **Question-1:** Which food scrap drop off location has highest rating. 

With the generated output file, I analyzed the highest rating food scrap drop off location using Tableau visualization as shown below,

![GitHub Logo](/images/NTA_Site_Rating.png)

### **Question-2:** How the rating frequency varies between borough in same NY city.

I found that, the rating frequency varies between different borough neighborhood. Some of the neighborhood with highest population has low rating count frequency and the neighborhood with lowest population has high rating count frequency. 

![GitHub Logo](/images/Population_Vs_Rating.png)

### **Question-3:** To check neighborhood counts, using different borough demographic information.

The neighborhood counts for each borough in the NYC demographic region is analyzed using Tableau geographic visualization.

![GitHub Logo](/images/Borough_NTA_Count.png)

### **Question-4:** Which Neighborhood Borough has highest rating.

The neighborhood borough with highest rating is found using below visual,

![GitHub Logo](/images/Rating_NTA_Borough.png)

## UI Application

The Python FLASK is used for creating UI application. The UI site shows three options for viewing which will be pulled from SQL database.

### Screen-1: Dashboard

Dashboard screen will list down the options for viewing food scrap site details

    http://localhost:5000/dashboard

![GitHub Logo](/images/Dashboard.png)

### Screen-2: Neighborhood Population List

This screen displays the list of borough and neighborhood with respective population count details.

    http://localhost:5000/ntaPopulation

![GitHub Logo](/images/NTA_population.png)

### Screen-3: Food Scrap Location List

This screen displays the list of food scrap drop off location along with the service vendor details.

    http://localhost:5000/getByFoodScrapDropOffLocation

![GitHub Logo](/images/FoodScrap_Location.png)

### Screen-4: Food Scrap Location List

This screen displays the list of food scrap drop off location grouped by rating details. The URL takes a rating parameter which extracts and displays the food scrap drop off location with that rating.

    http://localhost:5000/foodScrapLocationByRating?rating=4.0

![GitHub Logo](/images/FoodScrap_Site_Rating.png)



