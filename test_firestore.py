from firebase_config import db


def test_firestore_connection():
    doc_ref = db.collection("test").document("connection")
    payload = {
        "status": "Connected",
        "message": "Hello Firestore!",
    }

    doc_ref.set(payload)
    doc = doc_ref.get()

    assert doc.exists, "Expected Firestore document to exist."
    return doc.to_dict()


def main():
    try:
        document = test_firestore_connection()
        print("✅ Database connection successful!")
        print(document)
    except Exception as error:
        print("❌ Firestore test failed:", error)
        raise


if __name__ == "__main__":
    main()