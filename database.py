import sqlite3
from pathlib import Path
import pandas as pd
from datetime import datetime

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "data" / "tracker.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_db():

    c = conn()
    cur = c.cursor()

    # -------------------------
    # Tasks / Roadmap
    # -------------------------

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

    # -------------------------
    # Interview Questions
    # -------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS interview_questions (
            id INTEGER PRIMARY KEY,
            Category TEXT,
            Question TEXT,
            Difficulty TEXT,
            Status TEXT DEFAULT 'Not Practiced'
        )
    """)

    # -------------------------
    # English Practice
    # -------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS english_practice (
            Day INTEGER PRIMARY KEY,
            completed INTEGER DEFAULT 0
        )
    """)

    # -------------------------
    # Job Applications
    # -------------------------

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

    # VERY IMPORTANT:
    # Check interview questions AFTER tables are created.
    ensure_500_interview_questions()


# ============================================================
# 500 INTERVIEW QUESTIONS
# ============================================================

def ensure_500_interview_questions():

    c = conn()

    count = c.execute(
        "SELECT COUNT(*) FROM interview_questions"
    ).fetchone()[0]

    c.close()

    # Already 500 questions
    if count == 500:
        return

    # If database has 30 / 100 / any other number,
    # replace them with the complete 500-question bank.
    sync_500_interview_questions()


# ============================================================
# LOAD 500 QUESTIONS FROM CSV
# ============================================================

def sync_500_interview_questions():

    seed_file = BASE / "interview_questions_seed.csv"

    # --------------------------------------------------------
    # FIRST OPTION:
    # Load 500 questions from CSV
    # --------------------------------------------------------

    if seed_file.exists():

        try:

            df = pd.read_csv(seed_file)

            required_columns = [
                "id",
                "Category",
                "Question",
                "Difficulty"
            ]

            # Check CSV structure
            if all(col in df.columns for col in required_columns):

                df = df[required_columns].copy()

                # Remove empty questions
                df = df.dropna(subset=["Question"])

                # Remove duplicate questions
                df = df.drop_duplicates(
                    subset=["Question"]
                )

                # Keep exactly first 500
                df = df.head(500)

                # Only use CSV if it really contains 500
                if len(df) == 500:

                    c = conn()

                    # Remove old 30 questions
                    c.execute(
                        "DELETE FROM interview_questions"
                    )

                    for _, row in df.iterrows():

                        c.execute("""
                            INSERT INTO interview_questions
                            (
                                id,
                                Category,
                                Question,
                                Difficulty,
                                Status
                            )
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

            print(
                "CSV loading failed:",
                e
            )

    # --------------------------------------------------------
    # FALLBACK:
    # Generate 500 questions automatically
    # --------------------------------------------------------

    generate_builtin_500_questions()


# ============================================================
# BUILT-IN 500 QUESTION BANK
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
            "Python data types",
            "Lists and tuples",
            "Sets and dictionaries",
            "Functions",
            "Lambda functions",
            "Decorators",
            "Generators",
            "Iterators",
            "Exception handling",
            "File handling",
            "OOP",
            "Inheritance",
            "Polymorphism",
            "Encapsulation",
            "Modules",
            "Packages",
            "Virtual environments",
            "pip",
            "Type hints",
            "Dataclasses",
            "List comprehension",
            "Dictionary comprehension",
            "Context managers",
            "Memory management",
            "Garbage collection",
            "GIL",
            "Multithreading",
            "Multiprocessing",
            "Async programming",
            "Unit testing"
        ],

        "SQL": [
            "SELECT statements",
            "WHERE clause",
            "GROUP BY",
            "HAVING",
            "ORDER BY",
            "INNER JOIN",
            "LEFT JOIN",
            "RIGHT JOIN",
            "FULL JOIN",
            "Subqueries",
            "CTE",
            "Window functions",
            "ROW_NUMBER",
            "RANK",
            "DENSE_RANK",
            "Indexes",
            "Primary keys",
            "Foreign keys",
            "Normalization",
            "Transactions"
        ],

        "Statistics & Probability": [
            "Mean",
            "Median",
            "Mode",
            "Variance",
            "Standard deviation",
            "Covariance",
            "Correlation",
            "Probability",
            "Conditional probability",
            "Bayes theorem",
            "Normal distribution",
            "Binomial distribution",
            "Central Limit Theorem",
            "Confidence intervals",
            "Hypothesis testing",
            "p-value",
            "Type I error",
            "Type II error",
            "Sampling",
            "A/B testing"
        ],

        "Machine Learning": [
            "Supervised learning",
            "Unsupervised learning",
            "Semi-supervised learning",
            "Regression",
            "Classification",
            "Linear regression",
            "Logistic regression",
            "Decision trees",
            "Random forest",
            "Gradient boosting",
            "XGBoost",
            "LightGBM",
            "KNN",
            "K-means",
            "DBSCAN",
            "PCA",
            "Feature engineering",
            "Feature selection",
            "Data leakage",
            "Overfitting",
            "Underfitting",
            "Bias variance",
            "Regularization",
            "L1 regularization",
            "L2 regularization",
            "Cross validation",
            "Stratified cross validation",
            "Time series validation",
            "Train validation test",
            "Precision",
            "Recall",
            "F1 score",
            "ROC AUC",
            "PR AUC",
            "Confusion matrix",
            "MAE",
            "MSE",
            "RMSE",
            "R squared",
            "Missing values",
            "Categorical encoding",
            "Feature scaling",
            "Outliers",
            "Class imbalance",
            "SMOTE",
            "Hyperparameter tuning",
            "Grid search",
            "Random search",
            "Bayesian optimization",
            "Early stopping"
        ],

        "Deep Learning": [
            "Neural networks",
            "Neurons",
            "Weights",
            "Bias",
            "Forward propagation",
            "Backpropagation",
            "Loss functions",
            "Activation functions",
            "ReLU",
            "Sigmoid",
            "Tanh",
            "Softmax",
            "Vanishing gradient",
            "Exploding gradient",
            "Weight initialization",
            "Xavier initialization",
            "He initialization",
            "Dropout",
            "Batch normalization",
            "Layer normalization",
            "Epoch",
            "Batch size",
            "Iterations",
            "SGD",
            "Adam",
            "AdamW",
            "Learning rate",
            "Learning rate scheduling",
            "Early stopping",
            "Gradient clipping",
            "Transfer learning",
            "Fine tuning",
            "CNN",
            "RNN",
            "LSTM",
            "GRU",
            "Attention",
            "Transformers",
            "Positional encoding",
            "Encoder",
            "Decoder",
            "Seq2Seq",
            "Teacher forcing",
            "Perplexity",
            "GPU training",
            "Mixed precision",
            "Gradient accumulation",
            "Model checkpointing",
            "PyTorch",
            "TensorFlow"
        ],

        "Computer Vision": [
            "Image classification",
            "Object detection",
            "Image segmentation",
            "Semantic segmentation",
            "Instance segmentation",
            "CNN",
            "Convolution",
            "Kernel",
            "Stride",
            "Padding",
            "Pooling",
            "IoU",
            "NMS",
            "mAP",
            "YOLO",
            "Faster R-CNN",
            "Transfer learning",
            "Image augmentation",
            "Image normalization",
            "OCR"
        ],

        "NLP": [
            "Tokenization",
            "Stemming",
            "Lemmatization",
            "Stop words",
            "TF-IDF",
            "Bag of words",
            "N-grams",
            "Word embeddings",
            "Word2Vec",
            "GloVe",
            "Contextual embeddings",
            "NER",
            "POS tagging",
            "Sentiment analysis",
            "Text classification",
            "Seq2Seq",
            "Attention",
            "Transformers",
            "Masked language modeling",
            "Causal language modeling"
        ],

        "Generative AI / LLM": [
            "Generative AI",
            "Large Language Models",
            "Tokens",
            "Context window",
            "Transformer",
            "Self attention",
            "Query Key Value",
            "Multi-head attention",
            "Positional encoding",
            "Temperature",
            "Top-k",
            "Top-p",
            "Greedy decoding",
            "Beam search",
            "Prompt engineering",
            "Zero-shot prompting",
            "Few-shot prompting",
            "Structured output",
            "Function calling",
            "AI agents",
            "Hallucination",
            "Grounding",
            "Instruction tuning",
            "Fine tuning",
            "LoRA",
            "Quantization",
            "RLHF",
            "Model selection",
            "LLM cost",
            "LLM latency"
        ],

        "RAG / Vector DB": [
            "RAG",
            "Embeddings",
            "Vector database",
            "Semantic search",
            "Cosine similarity",
            "Chunking",
            "Chunk overlap",
            "Metadata filtering",
            "Dense retrieval",
            "Sparse retrieval",
            "Hybrid search",
            "Reranking",
            "Top-k retrieval",
            "Retrieval recall",
            "Context precision",
            "Context recall",
            "RAG evaluation",
            "Grounded answers",
            "Query rewriting",
            "Multi-query retrieval"
        ],

        "LangChain / LangGraph": [
            "LangChain",
            "Document loaders",
            "Text splitters",
            "Embeddings",
            "Retrievers",
            "Prompt templates",
            "Output parsers",
            "Chains",
            "LCEL",
            "LangGraph",
            "Graph workflows",
            "State",
            "Nodes",
            "Edges",
            "Conditional routing",
            "Human approval",
            "Tool calling",
            "Agent state",
            "Retries",
            "Agent loops"
        ],

        "Deployment / APIs / Docker": [
            "REST API",
            "FastAPI",
            "Request validation",
            "HTTP status codes",
            "CORS",
            "Docker",
            "Docker image",
            "Docker container",
            "Dockerfile",
            "Environment variables",
            "API keys",
            "Streamlit deployment",
            "Health checks",
            "Model serving",
            "Monitoring",
            "Inference latency",
            "Concurrency",
            "API versioning",
            "CI/CD",
            "Production deployment"
        ],

        "Projects / Real-world Scenarios": [
            "Explain your AI project",
            "Business problem",
            "Dataset collection",
            "Data validation",
            "Model selection",
            "Evaluation metrics",
            "Technical challenges",
            "Missing data",
            "Data leakage",
            "Model improvement",
            "Debugging",
            "Deployment",
            "Security",
            "Scalability",
            "Latency",
            "Monitoring",
            "Production failures",
            "Stakeholder communication",
            "Technical trade-offs",
            "Personal contribution"
        ],

        "HR / Behavioral": [
            "Tell me about yourself",
            "Why AI/ML",
            "Why this company",
            "Why job change",
            "Strengths",
            "Weakness",
            "Challenging project",
            "Failure and learning",
            "Deadline management",
            "Salary expectations"
        ]
    }

    questions = []

    question_id = 1

    for category, count in categories.items():

        topic_list = topics[category]

        for i in range(count):

            topic = topic_list[i % len(topic_list)]

            variations = [
                f"What is {topic}?",
                f"Explain {topic} with a practical AI/ML example.",
                f"How does {topic} work?",
                f"Why is {topic} important in an AI/ML project?",
                f"What are the advantages and limitations of {topic}?",
                f"How would you implement {topic} in a real project?",
                f"What common mistakes occur when using {topic}?",
                f"How would you debug a problem related to {topic}?",
                f"Compare {topic} with an alternative approach.",
                f"What interview follow-up questions can be asked about {topic}?"
            ]

            question = variations[i % len(variations)]

            # Make every question unique.
            if question in [x[2] for x in questions]:
                question = (
                    f"{question.rstrip('?')} "
                    f"(Interview Scenario {i + 1})?"
                )

            difficulty = (
                "Easy"
                if i % 3 == 0
                else "Medium"
                if i % 3 == 1
                else "Hard"
            )

            questions.append(
                (
                    question_id,
                    category,
                    question,
                    difficulty
                )
            )

            question_id += 1

    # Safety check
    if len(questions) != 500:

        raise ValueError(
            f"Expected 500 questions but generated {len(questions)}"
        )

    # Remove old questions
    c = conn()

    c.execute(
        "DELETE FROM interview_questions"
    )

    # Insert 500
    for qid, category, question, difficulty in questions:

        c.execute("""
            INSERT INTO interview_questions
            (
                id,
                Category,
                Question,
                Difficulty,
                Status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            qid,
            category,
            question,
            difficulty,
            "Not Practiced"
        ))

    c.commit()
    c.close()

    print("✅ 500 interview questions loaded successfully.")


# ============================================================
# LOAD ROADMAP TASKS
# ============================================================

def load_tasks():

    c = conn()

    df = pd.read_sql_query(
        "SELECT * FROM tasks ORDER BY Day, task_id",
        c
    )

    c.close()

    return df


# ============================================================
# LOAD INTERVIEW QUESTIONS
# ============================================================

def load_interview_questions():

    c = conn()

    df = pd.read_sql_query("""
        SELECT
            id,
            Category,
            Question,
            Difficulty,
            Status
        FROM interview_questions
        ORDER BY id
    """, c)

    c.close()

    return df


# ============================================================
# UPDATE INTERVIEW STATUS
# ============================================================

def update_interview_status(question_id, status):

    c = conn()

    c.execute("""
        UPDATE interview_questions
        SET Status = ?
        WHERE id = ?
    """, (
        status,
        int(question_id)
    ))

    c.commit()
    c.close()


# ============================================================
# ENGLISH PRACTICE
# ============================================================

def set_english_day(day, completed):

    c = conn()

    c.execute("""
        INSERT OR REPLACE INTO english_practice
        (
            Day,
            completed
        )
        VALUES (?, ?)
    """, (
        int(day),
        int(completed)
    ))

    c.commit()
    c.close()


def get_english_days():

    c = conn()

    rows = c.execute("""
        SELECT Day
        FROM english_practice
        WHERE completed = 1
    """).fetchall()

    c.close()

    return {row[0] for row in rows}


# ============================================================
# JOB APPLICATIONS
# ============================================================

def load_job_apps():

    c = conn()

    df = pd.read_sql_query("""
        SELECT *
        FROM job_applications
        ORDER BY id DESC
    """, c)

    c.close()

    return df


def add_job_app(
    company,
    role,
    source,
    location,
    status="Applied",
    notes=""
):

    c = conn()

    c.execute("""
        INSERT INTO job_applications
        (
            company,
            role,
            source,
            location,
            status,
            notes,
            applied_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        company,
        role,
        source,
        location,
        status,
        notes,
        datetime.now().strftime("%Y-%m-%d")
    ))

    c.commit()
    c.close()


def update_job_status(job_id, status):

    c = conn()

    c.execute("""
        UPDATE job_applications
        SET status = ?
        WHERE id = ?
    """, (
        status,
        int(job_id)
    ))

    c.commit()
    c.close()


def delete_job_app(job_id):

    c = conn()

    c.execute("""
        DELETE FROM job_applications
        WHERE id = ?
    """, (
        int(job_id),
    ))

    c.commit()
    c.close()


# ============================================================
# TASK STATUS
# ============================================================

def update_task_status(task_id, completed):

    c = conn()

    c.execute("""
        UPDATE tasks
        SET completed = ?
        WHERE task_id = ?
    """, (
        int(completed),
        int(task_id)
    ))

    c.commit()
    c.close()


# ============================================================
# REVISION
# ============================================================

def set_revision(task_id, revision_number, completed):

    column = f"revision_{int(revision_number)}"

    if column not in [
        "revision_1",
        "revision_2",
        "revision_3"
    ]:
        return

    c = conn()

    c.execute(
        f"""
        INSERT INTO revisions
        (
            task_id,
            {column}
        )
        VALUES (?, ?)
        ON CONFLICT(task_id)
        DO UPDATE SET {column} = excluded.{column}
        """,
        (
            int(task_id),
            int(completed)
        )
    )

    c.commit()
    c.close()


def get_revision_items():

    c = conn()

    df = pd.read_sql_query("""
        SELECT
            t.task_id,
            t.Day,
            t.Subject,
            t.Topic,
            COALESCE(r.revision_1, 0) AS revision_1,
            COALESCE(r.revision_2, 0) AS revision_2,
            COALESCE(r.revision_3, 0) AS revision_3
        FROM tasks t
        LEFT JOIN revisions r
        ON t.task_id = r.task_id
        WHERE t.completed = 1
        ORDER BY t.Day
    """, c)

    c.close()

    return df


# ============================================================
# METRICS
# ============================================================

def get_metrics():

    c = conn()

    # --------------------------------------------------------
    # Total Tasks
    # --------------------------------------------------------

    total = c.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    # --------------------------------------------------------
    # Completed Tasks
    # --------------------------------------------------------

    completed = c.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 1"
    ).fetchone()[0]

    # --------------------------------------------------------
    # Interview Questions Completed
    # --------------------------------------------------------

    interview_done = c.execute("""
        SELECT COUNT(*)
        FROM interview_questions
        WHERE Status != 'Not Practiced'
    """).fetchone()[0]

    # --------------------------------------------------------
    # Job Applications
    # --------------------------------------------------------

    jobs = c.execute(
        "SELECT COUNT(*) FROM job_applications"
    ).fetchone()[0]

    # --------------------------------------------------------
    # Overall Progress
    # --------------------------------------------------------

    overall = (
        completed / total * 100
        if total
        else 0
    )

    # --------------------------------------------------------
    # COMPLETED DAYS
    #
    # A day is counted as completed ONLY when
    # ALL tasks belonging to that day are completed.
    #
    # Example:
    # Day 1 -> 5 tasks -> 5 completed = 1 completed day
    # Day 2 -> 5 tasks -> 3 completed = 0 completed days
    # --------------------------------------------------------

    days_completed = c.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT Day
            FROM tasks
            GROUP BY Day
            HAVING COUNT(*) = SUM(
                CASE
                    WHEN completed = 1 THEN 1
                    ELSE 0
                END
            )
        )
    """).fetchone()[0]

    c.close()

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

    c = conn()

    df = pd.read_sql_query("""
        SELECT
            Subject,
            COUNT(*) AS Total,
            SUM(completed) AS Completed
        FROM tasks
        GROUP BY Subject
        ORDER BY Subject
    """, c)

    c.close()

    if df.empty:
        return df

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

    c = conn()

    df = pd.read_sql_query("""
        SELECT
            Week,
            COUNT(*) AS Total,
            SUM(completed) AS Completed
        FROM tasks
        GROUP BY Week
        ORDER BY Week
    """, c)

    c.close()

    if df.empty:
        return df

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

    c = conn()

    df = pd.read_sql_query("""
        SELECT
            Month,
            COUNT(*) AS Total,
            SUM(completed) AS Completed
        FROM tasks
        GROUP BY Month
        ORDER BY Month
    """, c)

    c.close()

    if df.empty:
        return df

    df["Progress"] = (
        df["Completed"] /
        df["Total"] *
        100
    )

    return df


# ============================================================
# RESET STUDY PROGRESS
# ============================================================

def reset_all_progress():

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

    c.execute("""
        DELETE FROM revisions
    """)

    c.commit()
    c.close()

