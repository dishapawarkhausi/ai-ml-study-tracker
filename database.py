
import os
import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "data" / "tracker.db"

_SUPABASE = None


# ============================================================
# PERSISTENT DATABASE
# ============================================================

def _get_supabase():
    """
    On Streamlit Community Cloud, use Supabase when
    SUPABASE_URL and SUPABASE_KEY are configured in Secrets.

    Locally, without those secrets, the app continues to use
    the bundled SQLite database.
    """
    global _SUPABASE

    if _SUPABASE is not None:
        return _SUPABASE

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    try:
        import streamlit as st

        if not url and "SUPABASE_URL" in st.secrets:
            url = st.secrets["SUPABASE_URL"]

        if not key and "SUPABASE_KEY" in st.secrets:
            key = st.secrets["SUPABASE_KEY"]
    except Exception:
        pass

    if url and key:
        try:
            from supabase import create_client
            _SUPABASE = create_client(url, key)
            return _SUPABASE
        except Exception as e:
            raise RuntimeError(
                "Supabase credentials were found, but the Supabase "
                f"client could not start: {e}"
            )

    return None


def using_supabase():
    return _get_supabase() is not None


# ============================================================
# LOCAL SQLITE FALLBACK
# ============================================================

def conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


# ============================================================
# INITIALIZE
# ============================================================

def init_db():

    sb = _get_supabase()

    if sb is not None:
        _ensure_remote_seeded()
        return

    c = conn()
    cur = c.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY,
            Day INTEGER,
            Week INTEGER,
            Month INTEGER,
            Subject TEXT,
            Topic TEXT,
            Subtopic TEXT,
            What_to_Learn TEXT,
            Study_Time TEXT,
            Practice_Time TEXT,
            Practice_Task TEXT,
            Interview_Time TEXT,
            Interview_Question TEXT,
            English_Time TEXT,
            English_Practice TEXT,
            Project_Work TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS interview_questions (
            id INTEGER PRIMARY KEY,
            Category TEXT,
            Question TEXT,
            Difficulty TEXT,
            Status TEXT DEFAULT 'Not Practiced'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS english_practice (
            Day INTEGER PRIMARY KEY,
            completed INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            role TEXT,
            source TEXT,
            location TEXT,
            status TEXT,
            notes TEXT,
            applied_date TEXT
        )
    """)

    c.commit()

    # Keep the existing 500-question system.
    if c.execute(
        "SELECT COUNT(*) FROM interview_questions"
    ).fetchone()[0] != 500:
        c.close()
        sync_500_interview_questions()
        return

    c.close()


# ============================================================
# REMOTE SEEDING
# ============================================================

def _remote_count(table):
    result = _get_supabase().table(table).select(
        "*", count="exact"
    ).limit(1).execute()
    return int(result.count or 0)


def _local_seed_rows():
    """
    Read the bundled SQLite database only for the first-time
    migration into Supabase. Existing Supabase data is never
    overwritten by this function.
    """
    if not DB_PATH.exists():
        return None, None, None, None

    c = sqlite3.connect(DB_PATH)

    tasks_df = pd.read_sql_query(
        "SELECT * FROM tasks ORDER BY task_id",
        c
    )

    questions_df = pd.read_sql_query(
        "SELECT * FROM interview_questions ORDER BY id",
        c
    )

    english_df = pd.read_sql_query(
        "SELECT * FROM english_practice ORDER BY Day",
        c
    )

    jobs_df = pd.read_sql_query(
        "SELECT * FROM job_applications ORDER BY id",
        c
    )

    c.close()

    return tasks_df, questions_df, english_df, jobs_df


def _clean(value):
    if pd.isna(value):
        return None
    if isinstance(value, bool):
        return bool(value)
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    return value


def _records(df):
    if df is None or df.empty:
        return []

    records = df.to_dict(orient="records")
    return [
        {k: _clean(v) for k, v in row.items()}
        for row in records
    ]


def _ensure_remote_seeded():

    sb = _get_supabase()

    # Tasks
    if _remote_count("tasks") == 0:

        tasks_df, _, _, _ = _local_seed_rows()

        if tasks_df is not None and not tasks_df.empty:

            mapped = tasks_df.rename(columns={
                "task_id": "task_id",
                "Day": "day",
                "Week": "week",
                "Month": "month",
                "Subject": "subject",
                "Topic": "topic",
                "Subtopic": "subtopic",
                "What_to_Learn": "what_to_learn",
                "Study_Time": "study_time",
                "Practice_Time": "practice_time",
                "Practice_Task": "practice_task",
                "Interview_Time": "interview_time",
                "Interview_Question": "interview_question",
                "English_Time": "english_time",
                "English_Practice": "english_practice",
                "Project_Work": "project_work",
                "completed": "completed",
            })

            sb.table("tasks").upsert(
                _records(mapped),
                on_conflict="task_id"
            ).execute()

    # Interview questions
    if _remote_count("interview_questions") == 0:

        _, questions_df, _, _ = _local_seed_rows()

        if questions_df is not None and not questions_df.empty:

            mapped = questions_df.rename(columns={
                "id": "id",
                "Category": "category",
                "Question": "question",
                "Difficulty": "difficulty",
                "Status": "status",
            })

            sb.table("interview_questions").upsert(
                _records(mapped),
                on_conflict="id"
            ).execute()

    # English practice
    if _remote_count("english_practice") == 0:

        _, _, english_df, _ = _local_seed_rows()

        if english_df is not None and not english_df.empty:

            mapped = english_df.rename(columns={
                "Day": "day",
                "completed": "completed",
            })

            sb.table("english_practice").upsert(
                _records(mapped),
                on_conflict="day"
            ).execute()

    # Job applications
    if _remote_count("job_applications") == 0:

        _, _, _, jobs_df = _local_seed_rows()

        if jobs_df is not None and not jobs_df.empty:

            mapped = jobs_df.rename(columns={
                "id": "id",
                "company": "company",
                "role": "role",
                "source": "source",
                "location": "location",
                "status": "status",
                "notes": "notes",
                "applied_date": "applied_date",
            })

            sb.table("job_applications").upsert(
                _records(mapped),
                on_conflict="id"
            ).execute()


# ============================================================
# 500 INTERVIEW QUESTIONS
# ============================================================

def ensure_500_interview_questions():

    if using_supabase():

        if _remote_count("interview_questions") != 500:
            sync_500_interview_questions()

        return

    c = conn()

    count = c.execute(
        "SELECT COUNT(*) FROM interview_questions"
    ).fetchone()[0]

    c.close()

    if count != 500:
        sync_500_interview_questions()


def sync_500_interview_questions():

    seed_file = BASE / "interview_questions_seed.csv"

    if seed_file.exists():

        try:

            df = pd.read_csv(seed_file)

            required_columns = [
                "id",
                "Category",
                "Question",
                "Difficulty"
            ]

            if all(
                col in df.columns
                for col in required_columns
            ):

                df = df[required_columns].copy()
                df = df.dropna(subset=["Question"])
                df = df.drop_duplicates(
                    subset=["Question"]
                ).head(500)

                if len(df) == 500:

                    if using_supabase():

                        records = []

                        for _, row in df.iterrows():

                            records.append({
                                "id": int(row["id"]),
                                "category": str(row["Category"]),
                                "question": str(row["Question"]),
                                "difficulty": str(row["Difficulty"]),
                                "status": "Not Practiced"
                            })

                        _get_supabase().table(
                            "interview_questions"
                        ).upsert(
                            records,
                            on_conflict="id"
                        ).execute()

                    else:

                        c = conn()

                        c.execute(
                            "DELETE FROM interview_questions"
                        )

                        for _, row in df.iterrows():

                            c.execute("""
                                INSERT INTO interview_questions
                                (id, Category, Question, Difficulty, Status)
                                VALUES (?, ?, ?, ?, ?)
                            """, (
                                int(row["id"]),
                                str(row["Category"]),
                                str(row["Question"]),
                                str(row["Difficulty"]),
                                "Not Practiced"
                            ))

                        c.commit()
                        c.close()

                    return

        except Exception as e:
            print("CSV loading failed:", e)

    generate_builtin_500_questions()


# ============================================================
# BUILT-IN FALLBACK
# ============================================================

def generate_builtin_500_questions():

    categories = {
        "Python": 60,
        "SQL": 40,
        "Statistics & Probability": 30,
        "Machine Learning": 80,
        "Deep Learning": 60,
        "Computer Vision": 30,
        "NLP": 30,
        "Generative AI / LLM": 60,
        "RAG / Vector DB": 35,
        "LangChain / LangGraph": 25,
        "Deployment / APIs / Docker": 20,
        "Projects / Real-world Scenarios": 20,
        "HR / Behavioral": 10
    }

    topics = {
        "Python": [
            "Python data types", "Lists and tuples",
            "Sets and dictionaries", "Functions",
            "Lambda functions", "Decorators", "Generators",
            "Iterators", "Exception handling", "File handling",
            "OOP", "Inheritance", "Polymorphism",
            "Encapsulation", "Modules", "Packages",
            "Virtual environments", "pip", "Type hints",
            "Dataclasses", "List comprehension",
            "Dictionary comprehension", "Context managers",
            "Memory management", "Garbage collection",
            "GIL", "Multithreading", "Multiprocessing",
            "Async programming", "Unit testing"
        ],
        "SQL": [
            "SELECT statements", "WHERE clause", "GROUP BY",
            "HAVING", "ORDER BY", "INNER JOIN", "LEFT JOIN",
            "RIGHT JOIN", "FULL JOIN", "Subqueries", "CTE",
            "Window functions", "ROW_NUMBER", "RANK",
            "DENSE_RANK", "Indexes", "Primary keys",
            "Foreign keys", "Normalization", "Transactions"
        ],
        "Statistics & Probability": [
            "Mean", "Median", "Mode", "Variance",
            "Standard deviation", "Covariance", "Correlation",
            "Probability", "Conditional probability",
            "Bayes theorem", "Normal distribution",
            "Binomial distribution", "Central Limit Theorem",
            "Confidence intervals", "Hypothesis testing",
            "p-value", "Type I error", "Type II error",
            "Sampling", "A/B testing"
        ],
        "Machine Learning": [
            "Supervised learning", "Unsupervised learning",
            "Semi-supervised learning", "Regression",
            "Classification", "Linear regression",
            "Logistic regression", "Decision trees",
            "Random forest", "Gradient boosting", "XGBoost",
            "LightGBM", "KNN", "K-means", "DBSCAN", "PCA",
            "Feature engineering", "Feature selection",
            "Data leakage", "Overfitting", "Underfitting",
            "Bias variance", "Regularization",
            "L1 regularization", "L2 regularization",
            "Cross validation", "Stratified cross validation",
            "Time series validation", "Train validation test",
            "Precision", "Recall", "F1 score", "ROC AUC",
            "PR AUC", "Confusion matrix", "MAE", "MSE",
            "RMSE", "R squared", "Missing values",
            "Categorical encoding", "Feature scaling", "Outliers",
            "Class imbalance", "SMOTE", "Hyperparameter tuning",
            "Grid search", "Random search",
            "Bayesian optimization", "Early stopping"
        ],
        "Deep Learning": [
            "Neural networks", "Neurons", "Weights", "Bias",
            "Forward propagation", "Backpropagation",
            "Loss functions", "Activation functions", "ReLU",
            "Sigmoid", "Tanh", "Softmax", "Vanishing gradient",
            "Exploding gradient", "Weight initialization",
            "Xavier initialization", "He initialization",
            "Dropout", "Batch normalization", "Layer normalization",
            "Epoch", "Batch size", "Iterations", "SGD", "Adam",
            "AdamW", "Learning rate", "Learning rate scheduling",
            "Early stopping", "Gradient clipping",
            "Transfer learning", "Fine tuning", "CNN", "RNN",
            "LSTM", "GRU", "Attention", "Transformers",
            "Positional encoding", "Encoder", "Decoder",
            "Seq2Seq", "Teacher forcing", "Perplexity",
            "GPU training", "Mixed precision",
            "Gradient accumulation", "Model checkpointing",
            "PyTorch", "TensorFlow"
        ],
        "Computer Vision": [
            "Image classification", "Object detection",
            "Image segmentation", "Semantic segmentation",
            "Instance segmentation", "CNN", "Convolution",
            "Kernel", "Stride", "Padding", "Pooling", "IoU",
            "NMS", "mAP", "YOLO", "Faster R-CNN",
            "Transfer learning", "Image augmentation",
            "Image normalization", "OCR"
        ],
        "NLP": [
            "Tokenization", "Stemming", "Lemmatization",
            "Stop words", "TF-IDF", "Bag of words", "N-grams",
            "Word embeddings", "Word2Vec", "GloVe",
            "Contextual embeddings", "NER", "POS tagging",
            "Sentiment analysis", "Text classification",
            "Seq2Seq", "Attention", "Transformers",
            "Masked language modeling", "Causal language modeling"
        ],
        "Generative AI / LLM": [
            "Generative AI", "Large Language Models", "Tokens",
            "Context window", "Transformer", "Self attention",
            "Query Key Value", "Multi-head attention",
            "Positional encoding", "Temperature", "Top-k",
            "Top-p", "Greedy decoding", "Beam search",
            "Prompt engineering", "Zero-shot prompting",
            "Few-shot prompting", "Structured output",
            "Function calling", "AI agents", "Hallucination",
            "Grounding", "Instruction tuning", "Fine tuning",
            "LoRA", "Quantization", "RLHF", "Model selection",
            "LLM cost", "LLM latency"
        ],
        "RAG / Vector DB": [
            "RAG", "Embeddings", "Vector database",
            "Semantic search", "Cosine similarity", "Chunking",
            "Chunk overlap", "Metadata filtering",
            "Dense retrieval", "Sparse retrieval", "Hybrid search",
            "Reranking", "Top-k retrieval", "Retrieval recall",
            "Context precision", "Context recall",
            "RAG evaluation", "Grounded answers",
            "Query rewriting", "Multi-query retrieval"
        ],
        "LangChain / LangGraph": [
            "LangChain basics", "Chains", "Prompts",
            "Output parsers", "Retrievers", "Document loaders",
            "Text splitters", "Vector stores", "Tools",
            "Agents", "Memory", "Callbacks", "LangGraph basics",
            "State", "Nodes", "Edges", "Conditional edges",
            "Checkpoints", "Human in the loop"
        ],
        "Deployment / APIs / Docker": [
            "FastAPI", "REST API", "Pydantic", "API endpoints",
            "Request validation", "Docker", "Dockerfile",
            "Images", "Containers", "Environment variables",
            "Deployment", "Logging", "Monitoring"
        ],
        "Projects / Real-world Scenarios": [
            "Project explanation", "Architecture design",
            "Data pipeline", "Model deployment",
            "Model monitoring", "Error handling",
            "Latency optimization", "Cost optimization",
            "Scaling", "Security"
        ],
        "HR / Behavioral": [
            "Tell me about yourself", "Why AI/ML",
            "Why are you changing jobs?", "Project experience",
            "Strengths", "Weaknesses", "Teamwork",
            "Conflict handling", "Career goals", "Salary expectation"
        ]
    }

    questions = []
    qid = 1

    for category, count in categories.items():

        topic_list = topics.get(category, [])

        for i in range(count):

            topic = (
                topic_list[i % len(topic_list)]
                if topic_list
                else category
            )

            difficulty = (
                "Easy"
                if i < count / 3
                else "Medium"
                if i < count * 2 / 3
                else "Hard"
            )

            questions.append({
                "id": qid,
                "category": category,
                "question": (
                    f"Explain {topic} and describe "
                    f"how you would use it in an AI/ML project."
                ),
                "difficulty": difficulty,
                "status": "Not Practiced"
            })

            qid += 1

    if using_supabase():

        _get_supabase().table(
            "interview_questions"
        ).upsert(
            questions,
            on_conflict="id"
        ).execute()

    else:

        c = conn()

        c.execute(
            "DELETE FROM interview_questions"
        )

        for q in questions:

            c.execute("""
                INSERT INTO interview_questions
                (id, Category, Question, Difficulty, Status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                q["id"],
                q["category"],
                q["question"],
                q["difficulty"],
                q["status"]
            ))

        c.commit()
        c.close()


# ============================================================
# TASKS
# ============================================================

def load_tasks():

    if using_supabase():

        data = (
            _get_supabase()
            .table("tasks")
            .select("*")
            .order("day")
            .order("task_id")
            .execute()
            .data
        )

        df = pd.DataFrame(data)

        if df.empty:
            return df

        return df.rename(columns={
            "day": "Day",
            "week": "Week",
            "month": "Month",
            "subject": "Subject",
            "topic": "Topic",
            "subtopic": "Subtopic",
            "what_to_learn": "What_to_Learn",
            "study_time": "Study_Time",
            "practice_time": "Practice_Time",
            "practice_task": "Practice_Task",
            "interview_time": "Interview_Time",
            "interview_question": "Interview_Question",
            "english_time": "English_Time",
            "english_practice": "English_Practice",
            "project_work": "Project_Work",
            "completed": "completed",
        })

    c = conn()

    df = pd.read_sql_query(
        "SELECT * FROM tasks ORDER BY Day, task_id",
        c
    )

    c.close()

    return df


def update_task_status(task_id, status):

    value = bool(int(status))

    if using_supabase():

        _get_supabase().table("tasks").update(
            {"completed": value}
        ).eq(
            "task_id", int(task_id)
        ).execute()

        return

    c = conn()

    c.execute(
        """
        UPDATE tasks
        SET completed = ?
        WHERE task_id = ?
        """,
        (int(value), int(task_id))
    )

    c.commit()
    c.close()


# ============================================================
# INTERVIEW
# ============================================================

def load_interview_questions():

    if using_supabase():

        data = (
            _get_supabase()
            .table("interview_questions")
            .select("*")
            .order("id")
            .execute()
            .data
        )

        df = pd.DataFrame(data)

        if df.empty:
            return df

        return df.rename(columns={
            "category": "Category",
            "question": "Question",
            "difficulty": "Difficulty",
            "status": "Status",
        })

    c = conn()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM interview_questions
        ORDER BY id
        """,
        c
    )

    c.close()

    return df


def update_interview_status(
    question_id,
    status
):

    if using_supabase():

        _get_supabase().table(
            "interview_questions"
        ).update(
            {"status": status}
        ).eq(
            "id", int(question_id)
        ).execute()

        return

    c = conn()

    c.execute(
        """
        UPDATE interview_questions
        SET Status = ?
        WHERE id = ?
        """,
        (status, int(question_id))
    )

    c.commit()
    c.close()


# ============================================================
# ENGLISH
# ============================================================

def set_english_day(day, completed):

    if using_supabase():

        _get_supabase().table(
            "english_practice"
        ).upsert(
            {
                "day": int(day),
                "completed": bool(completed)
            },
            on_conflict="day"
        ).execute()

        return

    c = conn()

    c.execute(
        """
        INSERT INTO english_practice
        (Day, completed)
        VALUES (?, ?)
        ON CONFLICT(Day)
        DO UPDATE SET completed = excluded.completed
        """,
        (int(day), int(bool(completed)))
    )

    c.commit()
    c.close()


def get_english_days():

    if using_supabase():

        data = (
            _get_supabase()
            .table("english_practice")
            .select("day,completed")
            .eq("completed", True)
            .execute()
            .data
        )

        return [
            int(row["day"])
            for row in data
        ]

    c = conn()

    rows = c.execute(
        """
        SELECT Day
        FROM english_practice
        WHERE completed = 1
        """
    ).fetchall()

    c.close()

    return [
        int(row[0])
        for row in rows
    ]


# ============================================================
# JOB TRACKER
# ============================================================

def load_job_apps():

    if using_supabase():

        data = (
            _get_supabase()
            .table("job_applications")
            .select("*")
            .order("id", desc=True)
            .execute()
            .data
        )

        return pd.DataFrame(data)

    c = conn()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM job_applications
        ORDER BY id DESC
        """,
        c
    )

    c.close()

    return df


def add_job_app(
    company,
    role,
    source,
    location,
    status,
    notes
):

    applied_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    row = {
        "company": company,
        "role": role,
        "source": source,
        "location": location,
        "status": status,
        "notes": notes,
        "applied_date": applied_date
    }

    if using_supabase():

        _get_supabase().table(
            "job_applications"
        ).insert(row).execute()

        return

    c = conn()

    c.execute(
        """
        INSERT INTO job_applications
        (company, role, source, location,
         status, notes, applied_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            company,
            role,
            source,
            location,
            status,
            notes,
            applied_date
        )
    )

    c.commit()
    c.close()


def update_job_status(
    job_id,
    status
):

    if using_supabase():

        _get_supabase().table(
            "job_applications"
        ).update(
            {"status": status}
        ).eq(
            "id", int(job_id)
        ).execute()

        return

    c = conn()

    c.execute(
        """
        UPDATE job_applications
        SET status = ?
        WHERE id = ?
        """,
        (status, int(job_id))
    )

    c.commit()
    c.close()


def delete_job_app(job_id):

    if using_supabase():

        _get_supabase().table(
            "job_applications"
        ).delete().eq(
            "id", int(job_id)
        ).execute()

        return

    c = conn()

    c.execute(
        """
        DELETE FROM job_applications
        WHERE id = ?
        """,
        (int(job_id),)
    )

    c.commit()
    c.close()


# ============================================================
# METRICS
# ============================================================

def get_metrics():

    tasks = load_tasks()

    if tasks.empty:

        total = 0
        completed = 0
        overall = 0
        days_completed = 0

    else:

        total = len(tasks)

        completed = int(
            tasks["completed"]
            .fillna(False)
            .astype(bool)
            .sum()
        )

        overall = (
            completed / total * 100
            if total
            else 0
        )

        days_completed = int(
            tasks.groupby("Day")["completed"]
            .all()
            .sum()
        )

    questions = load_interview_questions()

    if questions.empty:

        interview_done = 0

    else:

        interview_done = int(
            (
                questions["Status"]
                != "Not Practiced"
            ).sum()
        )

    jobs_df = load_job_apps()

    jobs = (
        len(jobs_df)
        if not jobs_df.empty
        else 0
    )

    return {
        "total": total,
        "completed": completed,
        "overall": overall,
        "days_completed": days_completed,
        "interview_done": interview_done,
        "jobs": jobs
    }


# ============================================================
# SUBJECT PROGRESS
# ============================================================

def get_subject_progress():

    tasks = load_tasks()

    if tasks.empty:
        return pd.DataFrame()

    df = (
        tasks.groupby("Subject")
        .agg(
            Total=("task_id", "count"),
            Completed=("completed", "sum")
        )
        .reset_index()
    )

    df["Progress"] = (
        df["Completed"] /
        df["Total"] *
        100
    )

    return df


# ============================================================
# WEEKLY PROGRESS
# ============================================================

def get_weekly_progress():

    tasks = load_tasks()

    if tasks.empty:
        return pd.DataFrame()

    df = (
        tasks.groupby("Week")
        .agg(
            Total=("task_id", "count"),
            Completed=("completed", "sum")
        )
        .reset_index()
    )

    df["Progress"] = (
        df["Completed"] /
        df["Total"] *
        100
    )

    return df


# ============================================================
# MONTHLY PROGRESS
# ============================================================

def get_monthly_progress():

    tasks = load_tasks()

    if tasks.empty:
        return pd.DataFrame()

    df = (
        tasks.groupby("Month")
        .agg(
            Total=("task_id", "count"),
            Completed=("completed", "sum")
        )
        .reset_index()
    )

    df["Progress"] = (
        df["Completed"] /
        df["Total"] *
        100
    )

    return df


# ============================================================
# RESET
# ============================================================

def reset_all_progress():

    if using_supabase():

        _get_supabase().table("tasks").update(
            {"completed": False}
        ).neq(
            "task_id", -1
        ).execute()

        _get_supabase().table(
            "interview_questions"
        ).update(
            {"status": "Not Practiced"}
        ).neq(
            "id", -1
        ).execute()

        _get_supabase().table(
            "english_practice"
        ).delete().neq(
            "day", -1
        ).execute()

        return

    c = conn()

    c.execute("""
        UPDATE tasks
        SET completed = 0
    """)

    c.execute("""
        UPDATE interview_questions
        SET Status = 'Not Practiced'
    """)

    c.execute("""
        DELETE FROM english_practice
    """)

    c.commit()
    c.close()
