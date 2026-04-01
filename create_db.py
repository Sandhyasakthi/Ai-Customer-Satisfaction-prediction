import os
from pymongo import MongoClient, errors

# Custom .env loader to avoid dependency issues for your review
def load_env():
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
        print(f"✅ Loaded configuration from {env_file}")

load_env()


def init_db():
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

    try:
        # Connect to MongoDB (local or cloud via env variable)
        mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=1000)
        
        # Test connection
        client.server_info()
        print(f"Successfully connected to MongoDB at {mongo_uri}")

        db = client["tata_steel_ai"]

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

    except errors.ServerSelectionTimeoutError as err:
        print("\nERROR: Could not connect to MongoDB.")
        print("Please ensure your local MongoDB server is running on port 27017.")
        print(f"Details: {err}\n")

if __name__ == "__main__":
    init_db()
