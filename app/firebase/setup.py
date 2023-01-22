from firebase_admin import credentials, initialize_app, firestore_async

import app.firebase as app_firebase


async def setup(cert):
    certificate = credentials.Certificate(cert)
    initialize_app(certificate)
    app_firebase.firebase_client = firestore_async.client()
