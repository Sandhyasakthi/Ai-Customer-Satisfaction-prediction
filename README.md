# AI-Driven Customer Satisfaction Prediction System

## Project Overview

The **AI-Driven Customer Satisfaction Prediction System** is a high-performance machine learning web application built for **Tata Steel**. It predicts customer satisfaction based on service-related inputs using a **CatBoost classifier**. The system features a modern, professional UI with real-time predictions and persistent storage using **MongoDB Atlas**.

Users can register, log in, submit service ratings, and view historical prediction reports and feedback on a unified dashboard.

---

## 🚀 Key Features

*   **Smart Authentication**: 
    *   **Case-Insensitive Login**: Access your account regardless of capitalization (e.g., `User@Email.com` and `user@email.com` are treated as the same).
    *   **Auto-Trimming**: Extra spaces are automatically removed from email and password during login.
    *   **Smart Feedback**: If an account is not found, the system now specifically tells the user and provides a one-click shortcut to switch to the **Sign Up** tab.
    *   **Manual Login after Signup**: Secure registration flow that redirects users back to login to manually verify their credentials.
*   **Real-time Prediction**: Leveraging a pre-trained **CatBoost model** (`model/catboost_model.cbm`) for instant results.
*   **Professional UI**: Glassmorphism design with a custom pastel palette and responsive interactive animations.
*   **Data Persistence**: All user accounts, service predictions, and feedback are securely stored in your **MongoDB Atlas** cluster.
*   **Comprehensive Reports**: Dashboard to analyze past predictions and monitor customer sentiment trends.

---

## 🛠️ Technologies Used

### Frontend
- **HTML5 & Semantic Elements**
- **Modern CSS**: Custom professional palette, glassmorphism, and responsive layouts.
- **Micro-animations**: Enhanced user engagement via hover effects and transitions.

### Backend
- **Python 3.10+**
- **Flask Framework**: Handling routing, customized authentication logic, and sessions.
- **Dotenv**: Managing environment variables like `MONGO_URI` and `SECRET_KEY`.

### Machine Learning
- **CatBoost Classifier**: High-performance gradient boosting for tabular data.
- **Scikit-learn**: Data preprocessing and model evaluation.
- **Pandas**: Data manipulation and feature engineering.

### Database
- **MongoDB Atlas**: Cloud-based NoSQL storage for users, predictions, and feedback.

---

## 📂 Project Structure

```text
Ai-Customer-Satisfaction-prediction/
│
├── model/                     # Machine Learning components
│   └── catboost_model.cbm     # The active trained model (354 KB)
│
├── static/                    # Static assets
│   └── style.css              # Custom professional glassmorphism styling
│
├── templates/                 # HTML templates (Flask/Jinja2)
│   ├── login_signup.html      # Smart Login & Signup
│   ├── dashboard.html         # User workspace
│   ├── predict.html           # Prediction Engine
│   ├── feedback.html          # Feedback system
│   └── reports.html           # Intelligence reports
│
├── app.py                    # Main Flask application entry point
├── create_db.py              # Script to initialize MongoDB collections
├── download_and_train.py     # Pipeline to fetch data & train model
├── .env.example              # Template for your MongoDB Atlas connection
├── requirements.txt           # Project dependencies
└── run_pipeline.bat          # Automation for retraining model
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- **Python 3.10+**
- **MongoDB Atlas Account** (Free tier works perfectly)

### 2. Clone the Repository
```bash
git clone https://github.com/Sandhyasakthi/Ai-Customer-Satisfaction-prediction.git
cd Ai-Customer-Satisfaction-prediction
```

### 3. Environment Configuration
1.  Locate the `.env.example` file in the root directory.
2.  Add your **MongoDB Atlas Connection String** and **Secret Key**.
3.  The project is configured to read these values directly to connect your cloud database.

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 📊 Training the Model
To retrain the model with fresh data:
1. Run the instruction pipeline:
   ```bash
   run_pipeline.bat
   ```
2. This will:
   - Download the latest dataset mirror (Airline Passenger Satisfaction).
   - Apply **SMOTE** to balance target classes.
   - Train a new **CatBoost model** and save it to `model/catboost_model.cbm`.

---

## 📝 Author
**Sandhya S**
*AI and Machine Learning Academic Project*
