import os
from pymongo import MongoClient, errors


def init_db():
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

    try:
        client.server_info()
    except errors.ServerSelectionTimeoutError as err:
        print("\nERROR: Could not connect to MongoDB.")
        print("Please ensure your local MongoDB server is running on port 27017 or set MONGO_URI.")
        print(f"Details: {err}\n")
        return

    db = client["tata_steel_ai"]
    users_collection = db["users"]
    users_collection.create_index("email", unique=True)

    test_email = "test@tatasteel.com"
    users_collection.update_one(
        {"email": test_email},
        {"$setOnInsert": {"name": "Test User", "password": "password123"}},
        upsert=True
    )

    print(f"MongoDB database initialized at {mongo_uri}")


if __name__ == "__main__":
    init_db()
