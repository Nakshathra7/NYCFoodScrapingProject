# NYCFoodScrapingProject
 
 # IA 626: Big Data Processing & Cloud Services - Final Project Documentation

## Project Title: 

#### Big Data Inspection - NYC Food Scrap Drop Off Location Analysis
 
## Project Description:

###### The main purpose of this project is to analyze the dataset which contains information about the food scrap drop off location in NYC and perform verious operations to understand the data. 

## ETL Process:

The food scrap drop off location is given for NYC boroughs and from the dataset using the latitude and longitude values, I am planning to pull the reviews and ratings for each location using google places API. The google places API requires placeid as parameter which will be extracted from google geocoding API first, then the placeid will be passed to places API for extracting reviews and ratings.

#### Google Geocoding API

    https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=YOUR_API_KEY

#### Google Places API

    https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name,rating,formatted_phone_number&key=YOUR_API_KEY

## Analysis/Filtering:

The main target of this project is to analyse the below questions for NYC food scrap dataset.

##### **Question-1:** Which food scrap drop off location has highest rating. 

##### **Question-2:** How the rating frequency varies between borough in same NY city.

##### **Question-3:** To check if there is correlation, using different borough demographic information.

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


