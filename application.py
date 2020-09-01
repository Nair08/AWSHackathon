from flask import Flask,render_template, request
import pymysql
import json
import urllib.request
import requests
application = Flask(__name__)

API_KEY = ""
GEOCODE_BASE_URL = "http://dev.virtualearth.net/REST/v1/Locations"

@application.route('/')
def hello_world():
    return render_template('hackathon.html')

@application.route('/references')
def api():
    return render_template('references.html')


@application.route('/getresults', methods=['GET'])
def temp():
    piecon = pymysql.connect('hackathon.cbwqiuux8uje.us-east-1.rds.amazonaws.com', 'hackathon', 'hackathon', 'hackdb')
    piecurr = pymysql.cursors.Cursor(piecon)
    year = request.args.get('year')
    pollutant = request.args.get('pollutant')
    pairs =  {
                "usepa-aqi": "aqi",
                "AQI": "aqi",
                "usepa-pm25":"pm25",
                "PM2.5": "pm25",
                "usepa-10": "pm10",
                "PM10": "pm10",
                "usepa-o3" : "o3",
                "Ozone": "o3",
                "usepa-no2" : "no2",
                "NitrogenDioxide": "no2",
                "usepa-so2" : "so2",
                "SulfurDioxide" : "so2",
                "usepa-co" : "co",
                "CarbonMonoxide" : "co"
              }

    print(year + ' ' + pollutant)
    print(pairs[pollutant])
    query = "select distinct (City),Country, max(max) from {} where Specie = '{}' group by City".format("y_"+year, pairs[pollutant])
    print(query)
    piecurr.execute(query)
    queryresults = piecurr.fetchall()
    print(queryresults)
    final_results = []
    for item in queryresults:
        if item:

            try:
                individualItem = []
                geocode_response = geocode(item[0] + " " + item[1])
                print(geocode_response)
                print(item[0], geocode_response[0], geocode_response[1])
                individualItem.append(geocode_response[0])
                individualItem.append(geocode_response[1])
                individualItem.append(item[2])
                final_results.append(individualItem)
            except Exception:
                pass
    queryresults = final_results
    return str(queryresults)

def geocode(address):
    # Join the parts of the URL together into one string.
    params = urllib.parse.urlencode({"q": address, "key": API_KEY,})
    url = f"{GEOCODE_BASE_URL}?{params}"

    result = json.load(urllib.request.urlopen(url))
    try:
        if result["statusDescription"] in ["OK"]:
            if result["resourceSets"][0]["resources"][0]["point"]["coordinates"]:
                return result["resourceSets"][0]["resources"][0]["point"]["coordinates"]
        else:
            print(address, " no geolocation")
    except Exception:
        pass
    #raise Exception(result["error_message"])


if __name__ == '__main__':
    application.debug = True
    application.run()
