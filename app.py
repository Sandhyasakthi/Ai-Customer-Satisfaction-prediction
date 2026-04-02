import os
from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient, errors
from catboost import CatBoostClassifier

# Custom .env loader to avoid dependency issues for your review
def load_env():
    # Attempt to load from .env first, fallback to .env.example if preferred by user
    env_file = ".env" if os.path.exists(".env") and os.path.getsize(".env") > 0 else ".env.example"
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
        print(f"✅ Loaded configuration from {env_file}")

load_env()

app = Flask(__name__)
app.secret_key = "tata_secret_key"


# ================= DATABASE =================

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

try:
    # Verify connection
    client.server_info()
    print("✅ Connected to MongoDB successfully.")
except errors.ServerSelectionTimeoutError as exc:
    print(f"⚠️ Warning: MongoDB connection delayed or failed: {exc}")
    # We don't exit here to allow the app to start on platforms like Render
    # where the MONGO_URI might be configured after the first deployment.

db = client["tata_steel_ai"]
users_collection = db["users"]
predictions_collection = db["predictions"]
feedback_collection = db["feedback"]

try:
    users_collection.create_index("email", unique=True)
except errors.PyMongoError:
    pass

users_collection.update_one(
    {"email": "test@tatasteel.com"},
    {"$setOnInsert": {"name": "Test User", "password": "password123"}},
    upsert=True
)


# ================= LOAD MODEL =================

model = CatBoostClassifier()
model.load_model("model/catboost_model.cbm")


def normalize_prediction(raw_prediction):
    # Unpack nested arrays returned by CatBoost
    if isinstance(raw_prediction, (list, tuple)) and len(raw_prediction) > 0:
        return normalize_prediction(raw_prediction[0])

    if hasattr(raw_prediction, "tolist"):
        try:
            return normalize_prediction(raw_prediction.tolist())
        except Exception:
            pass

    if isinstance(raw_prediction, bytes):
        raw_prediction = raw_prediction.decode("utf-8", errors="ignore")

    return raw_prediction


def get_prediction_label(raw_prediction):
    value = normalize_prediction(raw_prediction)
    text = str(value).strip()

    if text.isdigit():
        mapping = {
            0: "Satisfied",
            1: "Moderate",
            2: "Not Satisfied"
        }
        try:
            return mapping[int(text)]
        except (ValueError, KeyError):
            pass

    lower = text.lower()
    if lower in ["0", "not satisfied", "neutral or dissatisfied", "dissatisfied"]:
        return "Not Satisfied"
    if lower in ["1", "moderate", "neutral"]:
        return "Moderate"
    if lower in ["2", "satisfied"]:
        return "Satisfied"

    if "satisfied" in lower:
        return "Satisfied"
    if "not" in lower or "dissatisfied" in lower:
        return "Not Satisfied"

    return "Moderate"


# ================= LOGIN + SIGNUP =================

@app.route("/", methods=["GET","POST"])
def login_signup():

    if request.method == "POST":

        form_type = request.form.get("form_type", "login")
        email = request.form["email"].strip().lower()
        password = request.form["password"].strip()

        # Signup Mode
        if form_type == "signup":
            name = request.form.get("name", "").strip()
            
            if users_collection.find_one({"email": email}):
                return render_template("login_signup.html",
                                       error="User already exists")

            users_collection.insert_one({
                "name": name,
                "email": email,
                "password": password
            })
            # After signup, redirect to login mode with success message
            return render_template("login_signup.html", 
                                   success="Account created successfully! Please Log In.")

        # Login Mode
        user = users_collection.find_one({
            "email": email,
            "password": password
        })

        if user:
            session["user"] = user["name"]
            session["email"] = user["email"]
            return redirect("/dashboard")

        # If not found, check if the email exists at all to give better feedback
        if users_collection.find_one({"email": email}):
            return render_template("login_signup.html", 
                                   error="Invalid password. Please try again.")
        else:
            return render_template("login_signup.html",
                                   error="Account not found. Please click 'Sign Up' to create one.")

    return render_template("login_signup.html")


# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    return render_template("dashboard.html")


# ================= PREDICTION =================

@app.route("/predict", methods=["GET","POST"])
def predict():

    if "user" not in session:
        return redirect("/")

    result = None

    if request.method == "POST":

        service = int(request.form["service"])
        product = int(request.form["product"])
        delivery = int(request.form["delivery"])
        support = int(request.form["support"])
        price = int(request.form["price"])

        # Professional CatBoost Model native output processing
        raw_prediction = model.predict([[service, product, delivery, support, price]])
        result = get_prediction_label(raw_prediction)

        predictions_collection.insert_one({
            "user": session["user"],
            "service": service,
            "product": product,
            "delivery": delivery,
            "support": support,
            "price": price,
            "prediction": result
        })

    return render_template("predict.html", prediction=result)


# ================= FEEDBACK =================

@app.route("/feedback", methods=["GET","POST"])
def feedback():

    if "user" not in session:
        return redirect("/")

    if request.method == "POST":

        rating = request.form["rating"]
        comments = request.form["comments"]

        feedback_collection.insert_one({
            "user": session["user"],
            "rating": rating,
            "comments": comments
        })

        return render_template("feedback.html",
        success="Feedback Submitted")

    return render_template("feedback.html")


# ================= REPORTS =================

@app.route("/reports")
def reports():

    if "user" not in session:
        return redirect("/")

    predictions = list(predictions_collection.find({"user": session["user"]}))
    feedbacks = list(feedback_collection.find({"user": session["user"]}))

    return render_template(
        "reports.html",
        predictions=predictions,
        feedbacks=feedbacks
    )


# ================= LOGOUT =================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)