import json
import datetime
from google.cloud import firestore 
import requests
from requests.exceptions import HTTPError

from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return "home"

@app.route('/health')
def health_check():
    return 'OK'

@app.route('/fetch')
def fetch():
    return str(load_data())

@app.route('/<path:path>')
def catch_all(path):
    return "home"





db = firestore.Client.from_service_account_json(
        'PredictIt-9ad78fc7db12.json')

execs = 0
fails = 0
def load_data():

    global execs 
    global fails

    url = "https://www.predictit.org/api/marketdata/all/"
    try:
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')

        data = json.loads(response.content)
        added_markets = []
        ts = None

        for x in data["markets"]:
            if "tweet" in x["shortName"]:
                try:
                    doc_ref = db.collection(x["shortName"].replace('/', '.')).document(x["timeStamp"])
                    doc_ref.set(x)
                    added_markets.append(x["shortName"])
                    ts = x["timeStamp"]
                except Exception as err:
                    print(f'Other error occurred: {err}')
                    print(x["shortName"])

        execs += 1
        print("ran " + str(execs) + " times, failed " + str(fails) + " times")
        added_markets.append(ts)
        return added_markets

    fails += 1
    print("ran " + str(execs) + " times, failed " + str(fails) + " times")
    return 0



if __name__ == "__main__":
    app.run()