import json
import datetime
from google.cloud import firestore 
import requests
from requests.exceptions import HTTPError
import schedule
import time





db = firestore.Client.from_service_account_json(
        'PredictIt-9ad78fc7db12.json')
'''
# Project ID is determined by the GCLOUD_PROJECT environment variable
#db = firestore.Client()

doc_ref = db.collection('users').document('alovelace')
doc_ref.set({
    'first': 'Ada',
    'last': 'Lovelace',
    'born': 1815
})

doc_ref = db.collection('users').document('aturing')
doc_ref.set({
    'first': 'Alan',
    'middle': 'Mathison',
    'last': 'Turing',
    'born': 1912
})

users_ref = db.collection(u'users')
docs = users_ref.get()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))


'''
execs = 0
def load_data():
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
    #print(len(data["markets"]))
    c = 0
    for x in data["markets"]:
        try:
            doc_ref = db.collection(x["shortName"].replace('/', '.')).document(x["timeStamp"])
            doc_ref.set(x)
            c += 1
        except Exception as err:
            print(f'Other error occurred: {err}')
            print(x["shortName"])

    #print (c)
    global execs 
    execs += 1
    print("ran " + str(execs) + " times")
    return 1

schedule.every(60).seconds.do(load_data)


while 1:
    schedule.run_pending()
    time.sleep(1)