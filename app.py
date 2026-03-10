from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from catboost import CatBoostClassifier

app = Flask(__name__)
app.secret_key = "tata_secret_key"


# ================= DATABASE =================

client = MongoClient("mongodb://localhost:27017/")
db = client["tata_steel_ai"]

users_collection = db["users"]
predictions_collection = db["predictions"]
feedback_collection = db["feedback"]


# ================= LOAD MODEL =================

model = CatBoostClassifier()
model.load_model("model/catboost_model.cbm")


# ================= LOGIN + SIGNUP =================

@app.route("/", methods=["GET","POST"])
def login_signup():

    if request.method == "POST":

        Name = request.form.get("name")
        Email = request.form["email"]
        Password = request.form["password"]

        # Signup Mode
        if Name:

            if users_collection.find_one({"email":email}):
                return render_template("login_signup.html",
                error="User already exists")

            users_collection.insert_one({
                "name":Name,
                "email":Email,
                "password":Password
            })

            return redirect("/")

        # Login Mode
        user = users_collection.find_one({
            "email":Email,
            "password":Password
        })

        if user:
            session["user"] = user["name"]
            session["email"] = user["email"]
            return redirect("/dashboard")

        return render_template("login_signup.html",
        error="Invalid credentials")

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

        prediction = model.predict([[service,product,delivery,support]])[0]

        result = "Satisfied" if prediction == 1 else "Not Satisfied"

        predictions_collection.insert_one({
            "user":session["user"],
            "service":service,
            "product":product,
            "delivery":delivery,
            "support":support,
            "prediction":result
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
            "user":session["user"],
            "rating":rating,
            "comments":comments
        })

        return render_template("feedback.html",
        success="Feedback Submitted")

    return render_template("feedback.html")


# ================= REPORTS =================

@app.route("/reports")
def reports():

    if "user" not in session:
        return redirect("/")

    predictions = list(predictions_collection.find(
        {"user":session["user"]}
    ))

    feedbacks = list(feedback_collection.find(
        {"user":session["user"]}
    ))

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