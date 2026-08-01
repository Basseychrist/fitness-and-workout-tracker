import os

import firebase_admin
from firebase_admin import credentials, firestore

FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH", "firebase_key.json")

cred = credentials.Certificate(FIREBASE_KEY_PATH)

firebase_admin.initialize_app(cred)

db = firestore.client()