import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./bnode-2cd0d-firebase-adminsdk-eyxsn-c90ed335bb.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
docs = db.collection('users').get()
for doc in docs:
    print(doc.to_dict())

data = {
    u'name': u'Los Angeles',
    u'state': u'CA',
    u'country': u'USA'
}

# Add a new doc in collection 'cities' with ID 'LA'
db.collection(u'cities').document(u'LA').set(data)