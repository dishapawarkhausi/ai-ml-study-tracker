# 🤖 AI/ML Study Tracker

A complete **120-Day AI/ML Engineer Career Preparation & Progress Tracking application** built with **Python, Streamlit, SQLite, and Pandas**.

This application helps aspiring AI/ML Engineers organize their learning journey, track daily study progress, practice interview questions, improve technical English, manage job applications, and analyze overall career preparation progress — all from one dashboard.

---

## 🚀 Features

### 📊 Dashboard

The dashboard provides a complete overview of your AI/ML preparation journey.

* Overall learning progress
* Completed tasks
* Completed study days
* Job applications
* Interview questions practiced
* Daily focus
* Subject-wise progress
* 4-month career target

---

### 📅 Today's Plan

Follow your daily AI/ML learning plan step-by-step.

Each day can contain multiple tasks covering:

* 📚 Study
* 💻 Practice
* 🎤 Interview preparation
* 🗣️ English practice
* 🚀 Project work

Tasks can be marked as completed using interactive checkboxes.

A day is considered **completed only when all tasks for that day are completed**.

---

### 🗓️ 120-Day Roadmap

The project includes a structured **4-month / 120-day AI/ML Engineer roadmap**.

The roadmap is organized into:

* Months
* Weeks
* Days
* Subjects
* Topics
* Subtopics
* Study time
* Practice tasks
* Interview questions
* English practice
* Project work

### Roadmap Structure

```text
Month 1
├── Python
├── NumPy
├── Pandas
├── SQL
├── Mathematics
└── Machine Learning

Month 2
├── Deep Learning
├── PyTorch / TensorFlow
├── Computer Vision
└── NLP

Month 3
├── Generative AI
├── LLMs
├── Transformers
├── RAG
├── Vector Databases
├── LangChain
└── LangGraph

Month 4
├── AI/ML Projects
├── FastAPI
├── Docker
├── Deployment
├── Interview Preparation
└── Job Applications
```

---

## 🎤 Interview Preparation

The application includes an interview preparation system with **500 AI/ML interview questions**.

Questions cover:

* Python
* SQL
* Statistics & Probability
* Machine Learning
* Deep Learning
* Computer Vision
* NLP
* Generative AI / LLM
* RAG / Vector Databases
* LangChain / LangGraph
* Deployment / APIs / Docker
* Real-world AI/ML scenarios
* HR / Behavioral questions

### Interview Features

* Search questions
* Filter by category
* Filter by difficulty
* Filter by preparation status
* Track practiced questions
* Track confident questions

### Interview Status

```text
⬜ Not Practiced
🟡 Practiced
🟢 Confident
```

---

## 🗣️ English Practice

A dedicated **30-minute daily English practice system** designed for technical communication and interviews.

### Daily Routine

```text
10 Minutes → Read Aloud
10 Minutes → Technical Speaking
10 Minutes → Interview Speaking
```

The system provides AI/ML-related speaking topics and interview questions so that technical English improves alongside technical preparation.

---

## 💼 Job Application Tracker

Track AI/ML Engineer job applications directly inside the application.

### Application Information

* Company
* Role
* Source
* Location / Remote
* Status
* Notes
* Application date

### Application Status

```text
Applied
Recruiter Contact
Interview
Technical Round
HR Round
Rejected
Offer
Withdrawn
```

### Job Analytics

The application displays:

* Total applications
* Interviews
* Offers

---

## 📈 Learning Analytics

Track your preparation progress over time.

### Weekly Analytics

Displays:

* Total tasks
* Completed tasks
* Weekly progress

### Monthly Analytics

Displays:

* Total tasks
* Completed tasks
* Monthly progress

Charts are generated directly inside Streamlit.

---

## 🗄️ Database

The project uses **SQLite** for persistent local data storage.

The database stores:

### Tasks

```text
task_id
Day
Week
Month
Subject
Topic
Subtopic
What_to_Learn
Study_Time
Practice_Time
Practice_Task
Interview_Time
Interview_Question
English_Time
English_Practice
Project_Work
completed
```

### Interview Questions

```text
id
Category
Question
Difficulty
Status
```

### English Practice

```text
Day
completed
```

### Job Applications

```text
id
company
role
source
location
status
notes
applied_date
```

---

# 🛠️ Tech Stack

| Technology | Purpose                  |
| ---------- | ------------------------ |
| Python     | Application development  |
| Streamlit  | Web application UI       |
| Pandas     | Data processing          |
| SQLite     | Database                 |
| SQL        | Data storage and queries |
| HTML/CSS   | UI customization         |
| Git/GitHub | Version control          |

---

# 📁 Project Structure

```text
AI-ML-Career-Tracker/
│
├── app.py
├── database.py
├── interview_questions_seed.csv
│
├── data/
│   └── tracker.db
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/dishapawarkhausi/ai-ml-study-tracker.git
```

Move into the project directory:

```bash
cd AI-ML-Career-Tracker
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

Usually:

```text
http://localhost:8501
```

---

# 📦 requirements.txt

Example:

```text
streamlit
pandas
```

SQLite is included with Python, so it does not need to be installed separately.

---

# 🧠 How the Progress System Works

The project tracks progress at the **task level**.

For example:

```text
Day 1
├── Python Study        ✅
├── Python Practice     ✅
├── Interview Practice  ✅
├── English Practice    ✅
└── Project Work        ✅
```

When all tasks for Day 1 are completed:

```text
Days Completed = 1
```

If only 3 out of 5 tasks are completed:

```text
Day Progress = 60%
Days Completed = 0
```

This prevents partially completed days from being incorrectly counted as completed days.

---

# 🎯 Career Preparation Goal

The tracker is designed around a practical AI/ML Engineer preparation journey.

The main goal is to develop skills in:

```text
Python
   ↓
Data Analysis
   ↓
SQL
   ↓
Mathematics & Statistics
   ↓
Machine Learning
   ↓
Deep Learning
   ↓
Computer Vision
   ↓
NLP
   ↓
Generative AI
   ↓
LLMs
   ↓
RAG
   ↓
Vector Databases
   ↓
LangChain / LangGraph
   ↓
AI/ML Projects
   ↓
FastAPI
   ↓
Docker
   ↓
Deployment
   ↓
Interview Preparation
   ↓
Job Applications
```

---

# 💡 Why I Built This Project

Preparing for an AI/ML Engineer role requires managing multiple areas simultaneously:

* Technical learning
* Hands-on practice
* Projects
* Interview preparation
* Communication skills
* Job applications

Instead of using separate notebooks, spreadsheets, and applications, this project combines these activities into a single career preparation dashboard.

---

# 🔮 Future Improvements

Possible future versions can include:

* 🔐 User authentication
* ☁️ Cloud database
* 📱 Mobile-friendly interface
* 🔔 Daily reminders
* 🤖 AI-powered study assistant
* 🧠 AI-generated interview answers
* 📄 Resume analyzer
* 🎯 Job recommendation system
* 📊 Advanced analytics
* 📝 Personal notes for every topic
* 🔗 Job posting links
* 📅 Calendar integration
* 🌐 Online deployment
* 🤖 AI-powered career recommendations

---

# 📸 Application Modules

The application contains the following modules:

```text
🤖 AI/ML Tracker
│
├── 👩🏻‍💻 Dashboard
├── 📅 Today's Plan
├── 🗓️ 120-Day Roadmap
├── 🎤 Interview
├── 🗣️ English
├── 💼 Job Tracker
└── 📈 Analytics
```

---

# 🧪 Project Highlights

This project demonstrates practical experience with:

* Streamlit application development
* SQLite database management
* CRUD operations
* Pandas DataFrames
* Interactive data editors
* Progress tracking
* Data visualization
* Form handling
* Application state management
* SQL aggregation
* Modular Python development
* Career-oriented dashboard design

---

# 👩‍💻 Author

**Disha Pawar**

AI/ML Developer

Interested in:

* Artificial Intelligence
* Machine Learning
* Generative AI
* LLM Applications
* RAG
* Computer Vision
* NLP
* AI/ML Engineering

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is available for educational and portfolio purposes.
