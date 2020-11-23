#Flask Imports
from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 

from foodScrapNYC_BaseObject import baseObject

import pymysql, json, time

from flask_session import Session #Serverside Sessions

#Flask Sessions
app = Flask(__name__,static_url_path='')

SESSION_TYPE = 'filesystem'

app.config.from_object(__name__)
Session(app)

@app.route('/set')
def set():
    session['time'] = time.time()
    return 'set'
    
@app.route('/get')
def get():
    return str(session['time'])

@app.route('/')  
def dashboardMain():
    dashboardInfo = 'Hello... Welcome to Food Scrap Drop Off Location Details Site...!!!'
    return render_template('dashboard.html', title='Main Menu',msg=dashboardInfo)

#Routing Function to Dashboard Screen
@app.route('/dashboard')  
def dashboard():
    dashboardInfo = 'Hello... Welcome to Food Scrap Drop Off Location Details Site...!!!'
    return render_template('dashboard.html', title='Main Menu',msg=dashboardInfo)

#Routing Function to NTA (Neighborhood) Population Details Screen
@app.route('/ntaPopulation')
def ntaPopulation():
    fs = baseObject()
    fs.setupObject('manoha_ia626_foodscrapdropofflocations')
    fs.getByNTAName() 
    return render_template('ntaPopulation.html', title='NTA Population', ntaPopulations=fs.data)

#Routing Function to Food Scrap Drop Off Location Details Screen
@app.route('/getByFoodScrapDropOffLocation')
def getByFoodScrapDropOffLocation():
    fs = baseObject()
    fs.setupObject('manoha_ia626_foodscrapdropofflocations')  
    fs.getByFoodScrapDropOffLocation()  
    return render_template('foodScrapDropOffLocations.html', title='Food Scrap Drop Off Location Rating', foodScrapRatings=fs.data)   

#Routing Function to Food Scrap Site Rating Details Screen
@app.route('/foodScrapLocationByRating')  
def foodScrapLocationByRating():
    fs = baseObject()
    fs.setupObject('manoha_ia626_foodscrapdropofflocations') 
    fs.getByRating(request.args.get('rating'))  
    if (fs.data) == []:
        fs.getAllRating()    
        return render_template('ratingError.html', msg='No Rating is given.', allRatings=fs.data) 
    elif request.args.get('rating') != None and (fs.data) != '': 
        return render_template('foodScrapSiteRatingList.html', title='Food Scrap Drop Off Location Rating List', foodScrapSiteRatingLists=fs.data)

@app.route('/static/<path:path>') 
def send_static(path):  
    return send_from_directory('static', path)  
 
#Main Function Call
if __name__ == '__main__': 
   app.secret_key = '1234' 
   app.run(host='127.0.0.1',debug=True) 
  

    

