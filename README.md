# AI-Driven Customer Satisfaction Prediction System

## Project Overview

The **AI-Driven Customer Satisfaction Prediction System** is a high-performance machine learning web application built for **Tata Steel**. It predicts customer satisfaction based on service-related inputs using a **CatBoost classifier**. The system features a modern, professional UI with real-time predictions and persistent storage using **MongoDB**.

Users can register, log in, submit service ratings, and view historical prediction reports and feedback.

---

## 🚀 Key Features

*   **Real-time Prediction**: Leveraging a pre-trained CatBoost model for instant results.
*   **Professional UI**: Pastel-themed, responsive design with interactive animations.
*   **Secure Authentication**: User signup and login system with MongoDB integration.
*   **Data Persistence**: All predictions and customer feedback are stored for reporting.
*   **Training Pipeline**: Integrated scripts for downloading Kaggle datasets and retraining models.

---

## 🛠️ Technologies Used

### Frontend
- **HTML5 & Semantic Elements**
- **Modern CSS**: Custom pastel palette, glassmorphism, and responsive layouts.
- **Micro-animations**: Enhanced user engagement via hover effects and transitions.

### Backend
- **Python 3.10+**
- **Flask Framework**: Handling routing, sessions, and API endpoints.

### Machine Learning
- **CatBoost Classifier**: Optimized for tabular data and high accuracy.
- **Scikit-learn**: Used for data preprocessing (SMOTE) and evaluation.
- **Pandas**: Data manipulation and feature mapping.

### Database
- **MongoDB**: NoSQL storage for users, predictions, and feedback.

---

## 📂 Project Structure

```text
Ai-Customer-Satisfaction-prediction/
│
├── model/                     # Machine Learning components
│   └── catboost_model.cbm     # The active trained model
│
├── static/                    # Static assets
│   └── style.css              # Custom professional styling
│
├── templates/                 # HTML templates (Flask/Jinja2)
│   ├── login_signup.html
│   ├── dashboard.html
│   ├── predict.html
│   ├── feedback.html
│   └── reports.html
│
├── app.py                    # Main Flask application entry point
├── create_db.py              # Script to initialize MongoDB collections
├── download_and_train.py     # Pipeline to fetch Kaggle data & train model
├── requirements.txt           # Project dependencies
├── run_pipeline.bat          # Automation for retraining
└── push.bat                  # Deployment shortcut
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- **Python 3.10+**
- **MongoDB** (Local server running on port 27017 or a remote URI)

### 2. Clone the Repository
```bash
git clone https://github.com/Sandhyasakthi/Ai-Customer-Satisfaction-prediction.git
cd Ai-Customer-Satisfaction-prediction
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
Ensure MongoDB is running, then run:
```bash
python create_db.py
```

### 5. Run the Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 📊 Training the Model
To retrain the model with fresh data from the Kaggle dataset mirror:
1. Run the instruction pipeline:
   ```bash
   run_pipeline.bat
   ```
2. This will:
   - Download the latest dataset.
   - Apply SMOTE to balance classes.
   - Train a new CatBoost model.
   - Save it to `model/catboost_model.cbm`.

---

## 📝 Author
**Sandhya S**
*AI and Machine Learning Academic Project*
