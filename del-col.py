from google.cloud import firestore
import time
import sys

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).get()
    deleted = 0

    for doc in docs:
        #print(u'Deleting doc {}'.format(doc.id))
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

if len(sys.argv) > 1:
	skip = int(sys.argv[1])
else:
	skip = 0

db = firestore.Client.from_service_account_json(
        'PredictIt-9ad78fc7db12.json')

file = open("all-collections.txt")

lines = [line.rstrip('\n') for line in file]

for l in lines[skip:]:
	s = time.perf_counter()
	print(l)
	delete_collection(db.collection(l), 2500)
	t = time.perf_counter()
	print("deleted in " + str(t-s))
	print()