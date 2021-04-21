import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./bnode-2cd0d-firebase-adminsdk-eyxsn-c90ed335bb.json")
firebase_admin.initialize_app(cred)

