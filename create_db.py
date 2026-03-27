import os
import pymongo
import time

def init_db():
    try:
        # Connect to MongoDB (local or cloud via env variable)
        mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
        client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.server_info()
        print(f"Successfully connected to MongoDB at {mongo_uri}")

        db = client["tata_steel_ai"]

        # Drop existing collections completely for a fresh start (optional, good for testing)
        # db.drop_collection("users")
        # db.drop_collection("predictions")
        # db.drop_collection("feedback")

        users_collection = db["users"]
        predictions_collection = db["predictions"]
        feedback_collection = db["feedback"]

        # Create unique index on email
        users_collection.create_index("email", unique=True)

        # Insert a test user if it doesn't exist
        test_email = "test@tatasteel.com"
        if not users_collection.find_one({"email": test_email}):
            users_collection.insert_one({
                "name": "Test User",
                "email": test_email,
                "password": "password123"
            })
            print(f"Test user created: {test_email} / password123")
        else:
            print(f"Test user already exists: {test_email} / password123")

        print("MongoDB databases initialized successfully!")

    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("\nERROR: Could not connect to MongoDB.")
        print("Please ensure your local MongoDB server is running on port 27017.")
        print(f"Details: {err}\n")

if __name__ == "__main__":
    init_db()
