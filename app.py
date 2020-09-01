from flask import Flask,render_template, request
import pymysql
import json
import urllib.request
import requests
application = Flask(__name__)

API_KEY = ""
GEOCODE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

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
    query = "select distinct (City), max(max) from {} where Specie = '{}' group by City".format("y_"+year, pairs[pollutant])
    print(query)
    piecurr.execute(query)
    queryresults = piecurr.fetchall()
    print(queryresults)
    final_results = []
    for item in queryresults:
        individualItem = []
        geocode_response = geocode(item[0])
        print(geocode_response)
        print(item[1], geocode_response["lat"], geocode_response["lng"])
        individualItem.append(geocode_response["lat"])
        individualItem.append(geocode_response["lng"])
        individualItem.append(item[1])
        final_results.append(individualItem)
    queryresults = final_results
    return str(queryresults)

def geocode(address):
    # Join the parts of the URL together into one string.
    params = urllib.parse.urlencode({"address": address, "key": API_KEY,})
    url = f"{GEOCODE_BASE_URL}?{params}"

    result = json.load(urllib.request.urlopen(url))

    if result["status"] in ["OK"]:
        return result["results"][0]["geometry"]["location"]

    raise Exception(result["error_message"])


if __name__ == '__main__':
    application.debug = True
    application.run()
