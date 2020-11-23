#Import Declarations & Calling foodScrapNYC_BaseObject File to Access baseObject Class
import csv, requests, json, datetime, time, pymysql
import pandas as pd
from os import listdir
from os.path import isfile, join
from foodScrapNYC_BaseObject import baseObject

start1 = time.time()

n = 0

print("\nProcessing Food Scrap Drop Off Location Data ...\n")

#Clearing the Destination CSV files Before Execution
resultLocationFile = open('generatedFiles/LatLongLocation.csv', 'r')
resultLocationFile.close()
resultLocationFile = open('generatedFiles/LatLongLocation.csv', 'w')
resultLocationFile.write('')
resultLocationFile.close()

#Input CSV File Declaration - Merged CSV File of Two Datasets (FoodScrapDropOffLocation & NTANeighborhood Population Details)
NTAMergeCSVFile = 'generatedFiles/FoodScrap_Population_NTAName_Merge.csv'
NTAFoodScrapDetailsFile = open(NTAMergeCSVFile,'r')
reader = csv.reader(NTAFoodScrapDetailsFile)

#Declaring File Location For Accessing API Results (Latitude, Longitude and Rating Details)
latLongPath = 'generatedFiles/latlong/'
ratingPath = 'generatedFiles/rating/'

latLong = {}
ratingJSON = []

#Extracting File Names from the Path
for latLongFile in listdir(latLongPath):
    if '.json' in latLongFile:
        latLongDetails = latLongFile.split("_")
        latitude = latLongDetails[1]
        longtitudeSplit = latLongDetails[2].split(".json")
        longitude = longtitudeSplit[0]
        latLong[latitude] = longitude

for ratingFile in listdir(ratingPath):
    if '.json' in ratingFile:
        ratingJSON.append(ratingFile)

#Reading Input CSV File for Mapping Specific Fields to Destination CSV File
with open(NTAMergeCSVFile, 'r') as csvfile:
    start1 = time.time()
    csvreader = csv.reader(csvfile)

    #This Skips the First Row of the CSV File.
    next(csvreader)

    #Appending the Results to Output File
    with open('generatedFiles/LatLongLocation.csv', 'a') as latLongFile:
        writer = csv.writer(latLongFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Borough','Food_Scrap_Drop_Off_Site_Name','Latitude','Longitude','Location','NTAName','Serviced_by','Population','PlaceID','Rating'])

        #Reading Row by Row
        for row in csvreader:
            if row[23] != '':
                populationConvert = row[23].replace(',','')
            else:
                populationConvert = 0

            for latKey in latLong:
                if latKey == row[5]:
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
                    
                    n += 1 

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

#Creating Object to Access baseObject Class for Using SQL Functions
sqlProcessing = baseObject()
sqlProcessing.setupObject('manoha_ia626_foodscrapdropofflocations')

print ("\nTotal Time Taken for Execution: " + str(time.time() - start1))














