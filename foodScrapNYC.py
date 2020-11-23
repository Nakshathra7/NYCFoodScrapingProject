#Import Declarations
import csv, requests, json, datetime, time, pymysql
import pandas as pd

print("\nProcessing Food Scrap Drop Off Location Data ...\n")

n = 0

#Merging CSV File of Two Datasets (FoodScrapDropOffLocation & NTANeighborhood Population Details)
df1 = pd.read_csv("datasets/Food_Scrap_Drop-Off_Locations_in_NYC.csv")
df2 = pd.read_csv("datasets/New_York_City_Population_By_Neighborhood_Tabulation_Areas.csv")
merged = pd.merge(df1,df2, on="NTAName").fillna("")
merged.to_csv("generatedFiles/FoodScrap_Population_NTAName_Merge.csv", index=False)

#Input CSV File Declaration - Merged CSV File of Two Datasets
NTAMergeCSVFile = 'generatedFiles/FoodScrap_Population_NTAName_Merge.csv'
NTAFoodScrapDetailsFile = open(NTAMergeCSVFile,'r')
reader = csv.reader(NTAFoodScrapDetailsFile)

#Reading Input CSV File for Mapping Specific Fields to Destination CSV File
with open(NTAMergeCSVFile, 'r') as csvfile:
    start1 = time.time()

    csvreader = csv.reader(csvfile)

    #This Skips the First Row of the CSV File.
    next(csvreader)

    #Reading Row by Row
    for row in csvreader:
        if row[23] != '':
            populationConvert = row[23].replace(',','')
        else:
            populationConvert = 0

        #Checking If Latitude Row Values are not Empty
        if row[5] != '':
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
            
            n += 1 

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
            
print ("\nTotal Time Taken for Execution: " + str(time.time() - start1))











