# 🤖 AI/ML Engineer 120-Day Career Tracker

A complete **120-day AI/ML Engineer career preparation and interview tracking application** built with **Python and Streamlit**.

The application helps you manage your daily AI/ML learning, practice, interview preparation, English communication, job applications, and overall progress from one dashboard.

---

## 🚀 Live Application
https://aiml-study-tracker.streamlit.app/

## 🚀 Features

### 👩🏻‍💻 Dashboard

The dashboard provides an overview of your complete preparation journey.

It includes:

* Overall learning progress
* Completed topics
* Completed days
* Interview preparation progress
* Job application count
* Subject-wise progress
* 4-month career target

---

### 📅 Today's Plan

Follow your daily study plan from Day 1 to Day 120.

Each day contains:

* Study topics
* Study time
* Practice time
* Practice tasks
* Interview preparation
* English practice
* Project work
* Completion checkbox

You can tick the task after completing it.

---

### 🗓️ 120-Day Roadmap

The roadmap is divided into four months.

#### Month 1 — Fundamentals

* Python
* NumPy
* Pandas
* SQL
* Mathematics
* Machine Learning

#### Month 2 — Deep Learning

* Neural Networks
* TensorFlow
* PyTorch
* Computer Vision
* NLP
* CNN
* RNN/LSTM

#### Month 3 — Generative AI

* Generative AI
* LLMs
* Transformers
* Prompt Engineering
* Embeddings
* Vector Databases
* RAG
* LangChain
* LangGraph
* Hugging Face

#### Month 4 — Projects & Job Preparation

* AI/ML Projects
* GenAI Projects
* FastAPI
* Docker
* Deployment
* Git/GitHub
* Interview Preparation
* Resume Preparation
* Job Applications

---

## 🎤 Interview Preparation

The application includes **500 AI/ML interview questions**.

Questions cover areas such as:

* Python
* SQL
* Machine Learning
* Deep Learning
* NLP
* Computer Vision
* Generative AI
* LLMs
* Transformers
* RAG
* LangChain
* LangGraph
* Hugging Face
* Projects
* HR Interview

Each question can be marked as:

* ⬜ Not Practiced
* 🟡 Practiced
* 🟢 Confident

Interview progress is tracked automatically.

---

## 🗣️ English Practice

The application includes daily English practice to improve technical communication and interview confidence.

### Daily 30-Minute Routine

**10 minutes — Reading**

Read an AI/ML topic aloud.

**10 minutes — Technical Speaking**

Explain an AI/ML concept in your own words.

**10 minutes — Interview Speaking**

Practice answering AI/ML interview questions aloud.

---

## 💼 Job Tracker

Track your AI/ML job applications from one place.

You can record:

* Company
* Job role
* Location
* Application source
* Application status
* Notes

Supported statuses include:

* Applied
* Recruiter Contact
* Interview
* Technical Round
* HR Round
* Rejected
* Offer
* Withdrawn

---

## 📈 Analytics

Track your preparation progress using:

* Weekly progress
* Monthly progress
* Overall progress
* Subject-wise progress
* Interview progress
* Job application statistics

---

# ☁️ Persistent Cloud Database

The application supports **Supabase** for persistent cloud storage.

This is important when deploying the application on Streamlit Community Cloud.

Without a persistent database, local SQLite data can be lost when the application restarts or is redeployed.

With Supabase:

* ✅ Completed tasks remain completed
* ✅ Progress survives refresh
* ✅ Interview status remains saved
* ✅ English progress remains saved
* ✅ Job applications remain saved
* ✅ Data can be accessed from different devices

The application can also use the local SQLite database for local development when Supabase is not configured.

---

# 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* SQLite
* Supabase
* PostgreSQL
* SQL
* Git
* GitHub

---

# 📁 Project Structure

```text
AIML_Career/
│
├── app.py
├── database.py
├── requirements.txt
├── supabase_schema.sql
├── README.md
├── .gitignore
├── .env
│
├── data/
│   └── tracker.db
│
└── assets/
```

> `.env` and local database files should not be committed to GitHub.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/dishapawarkhausi/ai-ml-study-tracker.git
```

```bash
cd AI-ML-Study-Tracker
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file for local development.

```env
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_KEY=YOUR_SUPABASE_SERVICE_ROLE_KEY
```

### Important

Never commit your real `.env` file to GitHub.

The `.gitignore` file should contain:

```gitignore
.env
.streamlit/secrets.toml
*.db
*.sqlite
*.sqlite3
```

---

# 🗄️ Supabase Setup

1. Create a Supabase project.
2. Open the Supabase SQL Editor.
3. Open the project's:

```text
supabase_schema.sql
```

4. Run the SQL script.
5. Copy your Supabase project URL.
6. Copy the required Supabase API key.
7. Add them to your environment variables.

---

# ▶️ Run Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# ☁️ Deploy on Streamlit Community Cloud

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new application.
4. Select your GitHub repository.
5. Select:

```text
app.py
```

as the main file.
6. Deploy the application.

---

## 🔑 Streamlit Secrets

For the deployed application, add your Supabase credentials in:

```text
Streamlit Cloud
→ App Settings
→ Secrets
```

Use:

```toml
SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_SERVICE_ROLE_KEY"
```

Do **not** put these credentials directly inside `app.py`.

---

# 🎯 Project Goal

The goal of this application is to provide a single platform for preparing for an **AI/ML Engineer job within 120 days**.

The preparation combines:

```text
AI/ML Learning
       ↓
Daily Practice
       ↓
Projects
       ↓
Interview Preparation
       ↓
English Communication
       ↓
Job Applications
       ↓
Interview Tracking
       ↓
Job Search
```

---

# 📌 Recommended Daily Routine

A typical preparation day can include:

| Activity            | Suggested Time |
| ------------------- | -------------: |
| AI/ML Theory        |      2–3 hours |
| Coding Practice     |      1–2 hours |
| Project Work        |      1–2 hours |
| Interview Questions |  30–60 minutes |
| English Practice    |     30 minutes |
| Job Applications    |  30–60 minutes |

The exact schedule depends on the day's roadmap.

---

# 🔒 Security

Never commit the following to GitHub:

* Supabase service-role key
* API keys
* `.env`
* Streamlit secrets
* Passwords
* Private credentials
* Local database files containing private information

Use environment variables or Streamlit Secrets for credentials.

---

# 👩🏻‍💻 Author

**Disha Pawar**

AI/ML Developer

This project was created as a personal AI/ML career preparation and productivity application.

---

## ⭐ Future Improvements

Possible future features:

* Learning Hub with YouTube playlists and videos
* Topic-wise documentation
* Personal notes
* Study streaks
* Resume tracker
* Interview feedback tracker
* AI-powered interview practice
* AI mock interviews
* Daily reminders
* More analytics
* Personalized learning recommendations

---

## 📄 License

This project is intended for personal learning and career preparation.
