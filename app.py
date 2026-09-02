import streamlit as st
import pandas as pd
from database import *


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI/ML Engineer Career Tracker",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DATABASE
# ============================================================

init_db()

tasks = load_tasks()
metrics = get_metrics()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.9rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    [data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.18);
        border-radius: 14px;
        padding: 16px;
    }

    .tracker-title {
        font-size: 2.8rem;
        font-weight: 800;
    }

    .tracker-subtitle {
        color: #6b7280;
        font-size: .9rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🤖 AI/ML Tracker")

page = st.sidebar.radio(
    "Navigation",
    [
        "👩🏻‍💻 Dashboard",
        "📅 Today's Plan",
        "🗓️ 120-Day Roadmap",
        "🎤 Interview",
        "🗣️ English",
        "💼 Job Tracker",
        "📈 Analytics",
    ]
)

st.sidebar.divider()

st.sidebar.metric(
    "Overall Progress",
    f"{metrics['overall']:.1f}%"
)

st.sidebar.metric(
    "Topics Completed",
    f"{metrics['completed']}/{metrics['total']}"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_text(df, column, default=""):
    """
    Safely return a dataframe column.
    If the column does not exist, create it with a default value.
    """
    if column not in df.columns:
        df[column] = default

    return df[column]


def status_text(value):
    """
    Convert database 0/1 into user-friendly text.
    """
    try:
        return "✅ Completed" if int(value) == 1 else "⬜ Not Done"
    except Exception:
        return "⬜ Not Done"


# ============================================================
# TASK EDITOR
# ============================================================

def task_editor(df, key):

    view = df.copy()

    # Make sure required columns exist
    safe_text(view, "Subject")
    safe_text(view, "Topic")
    safe_text(view, "Subtopic")
    safe_text(view, "Study_Time")
    safe_text(view, "Practice_Time")
    safe_text(view, "Practice_Task")
    safe_text(view, "Interview_Time")
    safe_text(view, "Interview_Question")
    safe_text(view, "English_Time")
    safe_text(view, "English_Practice")
    safe_text(view, "Project_Work")
    safe_text(view, "What_to_Learn")
    safe_text(view, "completed", 0)

    # --------------------------------------------------------
    # Store original database IDs
    # --------------------------------------------------------

    original_ids = view["task_id"].tolist()

    original_done = (
        view["completed"]
        .fillna(0)
        .astype(bool)
        .tolist()
    )

    # --------------------------------------------------------
    # Create editable dataframe
    # --------------------------------------------------------

    editor_df = pd.DataFrame(
        {
            "Day": view["Day"],
            "Subject": view["Subject"],
            "Topic": view["Topic"],
            "Subtopic": view["Subtopic"],
            "Study Time": view["Study_Time"],
            "Practice Time": view["Practice_Time"],
            "Practice Task": view["Practice_Task"],
            "Interview Time": view["Interview_Time"],
            "Interview Question": view["Interview_Question"],
            "English Time": view["English_Time"],
            "English Practice": view["English_Practice"],
            "Project Work": view["Project_Work"],
            "Done": [
                bool(x)
                for x in view["completed"]
            ],
        }
    )

    # --------------------------------------------------------
    # Data editor
    # --------------------------------------------------------

    edited = st.data_editor(
        editor_df,

        column_config={

            "Day": st.column_config.NumberColumn(
                "Day",
                disabled=True
            ),

            "Subject": st.column_config.TextColumn(
                "Subject",
                disabled=True
            ),

            "Topic": st.column_config.TextColumn(
                "Topic",
                disabled=True
            ),

            "Subtopic": st.column_config.TextColumn(
                "Subtopic",
                disabled=True
            ),

            "Study Time": st.column_config.TextColumn(
                "Study Time",
                disabled=True
            ),

            "Practice Time": st.column_config.TextColumn(
                "Practice Time",
                disabled=True
            ),

            "Practice Task": st.column_config.TextColumn(
                "Practice Task",
                disabled=True
            ),

            "Interview Time": st.column_config.TextColumn(
                "Interview Time",
                disabled=True
            ),

            "Interview Question": st.column_config.TextColumn(
                "Interview Question",
                disabled=True
            ),

            "English Time": st.column_config.TextColumn(
                "English Time",
                disabled=True
            ),

            "English Practice": st.column_config.TextColumn(
                "English Practice",
                disabled=True
            ),

            "Project Work": st.column_config.TextColumn(
                "Project Work",
                disabled=True
            ),

            "Done": st.column_config.CheckboxColumn(
                "☑ Done",
                help="Tick this checkbox after completing the task.",
                default=False
            ),
        },

        disabled=[
            "Day",
            "Subject",
            "Topic",
            "Subtopic",
            "Study Time",
            "Practice Time",
            "Practice Task",
            "Interview Time",
            "Interview Question",
            "English Time",
            "English Practice",
            "Project Work",
        ],

        hide_index=True,

        use_container_width=True,

        key=key,
    )

    # --------------------------------------------------------
    # Save checkbox changes
    # --------------------------------------------------------

    changed = 0

    for i in range(len(edited)):

        new_done = bool(
            edited.iloc[i]["Done"]
        )

        old_done = bool(
            original_done[i]
        )

        if new_done != old_done:

            task_id = int(
                original_ids[i]
            )

            update_task_status(
                task_id,
                int(new_done)
            )

            changed += 1

    return changed


# ============================================================
# DASHBOARD
# ============================================================

if page == "👩🏻‍💻 Dashboard":

    st.markdown(
        '<div class="tracker-title">'
        '👩🏻‍💻 AI/ML Engineer Prep Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tracker-subtitle">'
        'Study • Practice • Interview • English • Jobs'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # Main Metrics
    # --------------------------------------------------------

    a, b, c, d, e = st.columns(5)

    a.metric(
        "📊 Overall",
        f"{metrics['overall']:.1f}%"
    )

    b.metric(
        "📚 Topics",
        f"{metrics['completed']}/{metrics['total']}"
    )

    c.metric(
        "📅 Days",
        metrics["days_completed"]
    )

    d.metric(
        "💼 Applications",
        metrics["jobs"]
    )

    e.metric(
        "🎤 Interview Que.",
        metrics["interview_done"]
    )

    st.write("")

    st.progress(
        float(metrics["overall"] / 100)
    )

    st.caption(
        f"You have completed "
        f"{metrics['overall']:.1f}% of your roadmap."
    )

    # --------------------------------------------------------
    # Today's Focus
    # --------------------------------------------------------

    st.subheader("📌 Today's Focus")

    day_number = st.number_input(
        "Select Day",
        min_value=1,
        max_value=120,
        value=1,
        step=1
    )

    today_df = tasks[
        tasks["Day"] == day_number
    ].copy()

    if today_df.empty:

        st.info(
            "No tasks available for this day."
        )

    else:

        pct = float(
            today_df["completed"]
            .fillna(0)
            .mean()
        )

        x, y = st.columns(
            [4, 1]
        )

        with x:

            st.progress(pct)

        with y:

            st.metric(
                f"Day {day_number}",
                f"{pct * 100:.0f}%"
            )

        display_today = today_df.copy()

        # Safely create missing columns
        for col in [
            "Subject",
            "Topic",
            "Subtopic",
            "Study_Time",
            "Practice_Time",
            "Interview_Time",
            "English_Time",
            "completed"
        ]:

            if col not in display_today.columns:

                display_today[col] = ""

        display_today = display_today[
            [
                "Subject",
                "Topic",
                "Subtopic",
                "Study_Time",
                "Practice_Time",
                "Interview_Time",
                "English_Time",
                "completed",
            ]
        ].copy()

        display_today["completed"] = (
            display_today["completed"]
            .apply(status_text)
        )

        display_today.rename(
            columns={
                "Study_Time": "Study Time",
                "Practice_Time": "Practice Time",
                "Interview_Time": "Interview Time",
                "English_Time": "English Time",
                "completed": "Done",
            },
            inplace=True
        )

        st.dataframe(
            display_today,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # Subject Progress
    # --------------------------------------------------------

    st.subheader(
        "📊 Subject Progress"
    )

    prog = get_subject_progress()

    if not prog.empty:

        cols = st.columns(3)

        for i, row in prog.iterrows():

            with cols[i % 3]:

                st.write(
                    f"**{row['Subject']}** — "
                    f"{row['Progress']:.0f}%"
                )

                st.progress(
                    float(
                        row["Progress"] / 100
                    )
                )

    # --------------------------------------------------------
    # 4 Month Target
    # --------------------------------------------------------

    st.subheader(
        "🎯 4-Month Target"
    )

    targets = [
        (
            "Month 1",
            "Python + NumPy + Pandas + SQL + Mathematics + Machine Learning"
        ),
        (
            "Month 2",
            "Deep Learning + PyTorch/TensorFlow + Computer Vision + NLP"
        ),
        (
            "Month 3",
            "Generative AI + LLMs + Transformers + RAG + LangChain + LangGraph"
        ),
        (
            "Month 4",
            "Projects + FastAPI + Docker + Deployment + Interviews + Job Applications"
        ),
    ]

    for month_name, description in targets:

        st.markdown(
            f"**{month_name}:** {description}"
        )


# ============================================================
# TODAY'S PLAN
# ============================================================

elif page == "📅 Today's Plan":

    st.title(
        "📅 Today's Plan"
    )

    st.caption(
        "Follow the plan step-by-step and tick each task after completing it."
    )

    day = st.number_input(
        "Select Study Day",
        min_value=1,
        max_value=120,
        value=1,
        step=1,
        key="today_day"
    )

    df = tasks[
        tasks["Day"] == day
    ].copy()

    if df.empty:

        st.warning(
            "No tasks found for this day."
        )

    else:

        completed = int(
            df["completed"]
            .fillna(0)
            .sum()
        )

        total = len(df)

        percentage = (
            completed / total
            if total
            else 0
        )

        a, b = st.columns(2)

        with a:

            st.metric(
                "Today's Tasks",
                total
            )

        with b:

            st.metric(
                "Completed",
                f"{completed}/{total}"
            )

        st.progress(
            percentage
        )

        st.info(
            "☑ Tick the Done checkbox only after you finish that task."
        )

        changed = task_editor(
            df,
            f"today_editor_{day}"
        )

        if changed:

            st.success(
                f"✅ {changed} task(s) updated successfully."
            )

            st.rerun()


# ============================================================
# 120-DAY ROADMAP
# ============================================================

elif page == "🗓️ 120-Day Roadmap":

    st.title(
        "🗓️ 120-Day AI/ML Engineer Roadmap"
    )

    st.caption(
        "Your complete 4-month learning roadmap."
    )

    month = st.selectbox(
        "Select Month",
        [1, 2, 3, 4],
        format_func=lambda x: f"Month {x}"
    )

    df = tasks[
        tasks["Month"] == month
    ].copy()

    if df.empty:

        st.info(
            "No tasks found for this month."
        )

    else:

        # ----------------------------------------------------
        # Month Progress
        # ----------------------------------------------------

        month_completed = int(
            df["completed"]
            .fillna(0)
            .sum()
        )

        month_total = len(df)

        month_progress = (
            month_completed / month_total
            if month_total
            else 0
        )

        st.metric(
            f"Month {month}",
            f"{month_completed}/{month_total} "
            f"({month_progress * 100:.0f}%)"
        )

        st.progress(
            month_progress
        )

        st.divider()

        # ----------------------------------------------------
        # Week-wise roadmap
        # ----------------------------------------------------

        for week in sorted(
            df["Week"]
            .dropna()
            .unique()
        ):

            w = df[
                df["Week"] == week
            ].copy()

            pct = (
                w["completed"]
                .fillna(0)
                .mean()
            )

            st.markdown(
                f"### 📘 Week {int(week)}"
            )

            st.progress(
                float(pct)
            )

            st.caption(
                f"Week progress: "
                f"{pct * 100:.0f}%"
            )

            # ------------------------------------------------
            # Safely prepare columns
            # ------------------------------------------------

            for col in [
                "Day",
                "Subject",
                "Topic",
                "Subtopic",
                "Study_Time",
                "Practice_Time",
                "Project_Work",
                "completed"
            ]:

                if col not in w.columns:

                    w[col] = ""

            display_week = w[
                [
                    "Day",
                    "Subject",
                    "Topic",
                    "Subtopic",
                    "Study_Time",
                    "Practice_Time",
                    "Project_Work",
                    "completed",
                ]
            ].copy()

            display_week["completed"] = (
                display_week["completed"]
                .apply(status_text)
            )

            display_week.rename(
                columns={
                    "Study_Time": "Study Time",
                    "Practice_Time": "Practice Time",
                    "Project_Work": "Project Work",
                    "completed": "Done",
                },
                inplace=True
            )

            st.dataframe(
                display_week,
                use_container_width=True,
                hide_index=True
            )

            st.divider()


# ============================================================
# INTERVIEW PREPARATION
# ============================================================

elif page == "🎤 Interview":

    st.title(
        "🎤 AI/ML Interview Preparation"
    )

    st.caption(
        "Prepare all 500 interview questions and track your confidence."
    )

    qdf = load_interview_questions()

    if qdf.empty:

        st.warning(
            "No interview questions available."
        )

    else:

        # ----------------------------------------------------
        # Metrics
        # ----------------------------------------------------

        total_questions = len(qdf)

        practiced = int(
            (
                qdf["Status"]
                != "Not Practiced"
            ).sum()
        )

        confident = int(
            (
                qdf["Status"]
                == "Confident"
            ).sum()
        )

        a, b, c = st.columns(3)

        a.metric(
            "📚 Total Questions",
            total_questions
        )

        b.metric(
            "✅ Practiced",
            practiced
        )

        c.metric(
            "🎯 Confident",
            confident
        )

        overall_interview_progress = (
            practiced / total_questions
            if total_questions
            else 0
        )

        st.progress(
            overall_interview_progress
        )

        st.caption(
            f"{practiced}/{total_questions} "
            f"questions practiced"
        )

        st.divider()

        # ----------------------------------------------------
        # Category Filter
        # ----------------------------------------------------

        categories = [
            "All"
        ] + sorted(
            qdf["Category"]
            .dropna()
            .unique()
        )

        category = st.selectbox(
            "📚 Category",
            categories
        )

        if category != "All":

            qdf = qdf[
                qdf["Category"]
                == category
            ]

        # ----------------------------------------------------
        # Difficulty Filter
        # ----------------------------------------------------

        if "Difficulty" in qdf.columns:

            difficulties = [
                "All"
            ] + sorted(
                qdf["Difficulty"]
                .dropna()
                .unique()
            )

            difficulty = st.selectbox(
                "🎯 Difficulty",
                difficulties
            )

            if difficulty != "All":

                qdf = qdf[
                    qdf["Difficulty"]
                    == difficulty
                ]

        # ----------------------------------------------------
        # Status Filter
        # ----------------------------------------------------

        status_filter = st.selectbox(
            "📌 Status",
            [
                "All",
                "Not Practiced",
                "Practiced",
                "Confident"
            ]
        )

        if status_filter != "All":

            qdf = qdf[
                qdf["Status"]
                == status_filter
            ]

        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------

        search = st.text_input(
            "🔎 Search Interview Question",
            placeholder=(
                "Search Python, RAG, SQL, "
                "Machine Learning, LLM..."
            )
        )

        if search.strip():

            text = (
                search
                .strip()
                .lower()
            )

            qdf = qdf[
                qdf["Question"]
                .astype(str)
                .str.lower()
                .str.contains(
                    text,
                    regex=False,
                    na=False
                )
            ]

        st.write(
            f"Showing **{len(qdf)}** questions."
        )

        # ----------------------------------------------------
        # Questions
        # ----------------------------------------------------

        for _, row in qdf.iterrows():

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**Q{int(row['id'])}. "
                    f"{row['Question']}**"
                )

                st.caption(
                    f"📚 {row['Category']} "
                    f" • 🎯 {row['Difficulty']}"
                )

                options = [
                    "Not Practiced",
                    "Practiced",
                    "Confident"
                ]

                current = (
                    row["Status"]
                    if row["Status"]
                    in options
                    else "Not Practiced"
                )

                choice = st.radio(
                    "Preparation Status",
                    options,
                    index=options.index(
                        current
                    ),
                    horizontal=True,
                    key=(
                        f"interview_"
                        f"{int(row['id'])}"
                    )
                )

                if choice != current:

                    update_interview_status(
                        int(row["id"]),
                        choice
                    )

                    st.rerun()


# ============================================================
# ENGLISH PRACTICE
# ============================================================

elif page == "🗣️ English":

    st.title(
        "🗣️ Daily English Practice"
    )

    st.caption(
        "30 minutes every day to improve technical English and interview communication."
    )

    day = st.number_input(
        "Practice Day",
        min_value=1,
        max_value=120,
        value=1,
        step=1,
        key="english_day"
    )

    df = tasks[
        tasks["Day"] == day
    ].copy()

    if df.empty:

        st.info(
            "No English content available for this day."
        )

    else:

        st.subheader(
            "⏱️ 30-Minute English Routine"
        )

        st.markdown(
            "### 📖 10 Minutes — Read Aloud"
        )

        st.write(
            "Read today's AI/ML topic aloud in English."
        )

        st.markdown(
            "### 🗣️ 10 Minutes — Technical Speaking"
        )

        vals = [
            x
            for x in df[
                "English_Practice"
            ]
            .astype(str)
            .tolist()
            if x.strip()
        ]

        if vals:

            for value in vals[:3]:

                st.write(
                    f"• {value}"
                )

        else:

            st.write(
                "Explain today's technical topic in your own words."
            )

        st.markdown(
            "### 🎤 10 Minutes — Interview Speaking"
        )

        questions = [
            x
            for x in df[
                "Interview_Question"
            ]
            .astype(str)
            .tolist()
            if x.strip()
        ]

        if questions:

            for question in questions[:3]:

                st.write(
                    f"• {question}"
                )

        else:

            st.write(
                "Practice answering one AI/ML interview question aloud."
            )

        st.divider()

        already = (
            day
            in get_english_days()
        )

        checked = st.checkbox(
            "☑ I completed today's English practice",
            value=already,
            key=f"english_completed_{day}"
        )

        if checked != already:

            set_english_day(
                day,
                checked
            )

            st.rerun()


# ============================================================
# JOB TRACKER
# ============================================================

elif page == "💼 Job Tracker":

    st.title(
        "💼 Job Application Tracker"
    )

    st.caption(
        "Track every AI/ML Engineer application."
    )

    jobs = load_job_apps()

    status_options = [
        "Applied",
        "Recruiter Contact",
        "Interview",
        "Technical Round",
        "HR Round",
        "Rejected",
        "Offer",
        "Withdrawn"
    ]

    # --------------------------------------------------------
    # Application Statistics
    # --------------------------------------------------------

    if not jobs.empty:

        total_jobs = len(jobs)

        interviews = len(
            jobs[
                jobs["status"].isin(
                    [
                        "Interview",
                        "Technical Round",
                        "HR Round"
                    ]
                )
            ]
        )

        offers = len(
            jobs[
                jobs["status"]
                == "Offer"
            ]
        )

        a, b, c = st.columns(3)

        a.metric(
            "📨 Applications",
            total_jobs
        )

        b.metric(
            "🎤 Interviews",
            interviews
        )

        c.metric(
            "🎉 Offers",
            offers
        )

        st.divider()

        # ----------------------------------------------------
        # Existing Applications
        # ----------------------------------------------------

        st.subheader(
            "📋 Applications"
        )

        for _, row in jobs.iterrows():

            with st.container(
                border=True
            ):

                c1, c2, c3 = st.columns(
                    [2, 2, 1]
                )

                with c1:

                    st.markdown(
                        f"**{row['company']}**"
                    )

                with c2:

                    st.write(
                        row["role"]
                    )

                with c3:

                    st.write(
                        row["status"]
                    )

                current_index = (
                    status_options.index(
                        row["status"]
                    )
                    if row["status"]
                    in status_options
                    else 0
                )

                new_status = st.selectbox(
                    "Update Status",
                    status_options,
                    index=current_index,
                    key=(
                        f"status_"
                        f"{row['id']}"
                    )
                )

                if new_status != row["status"]:

                    update_job_status(
                        int(row["id"]),
                        new_status
                    )

                    st.rerun()

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{row['id']}"
                ):

                    delete_job_app(
                        int(row["id"])
                    )

                    st.rerun()

    else:

        st.info(
            "No job applications added yet."
        )

    # --------------------------------------------------------
    # Add Application
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "➕ Add New Application"
    )

    with st.form(
        "add_job"
    ):

        c1, c2 = st.columns(2)

        company = c1.text_input(
            "Company"
        )

        role = c2.text_input(
            "Role"
        )

        c3, c4 = st.columns(2)

        source = c3.selectbox(
            "Source",
            [
                "Naukri",
                "LinkedIn",
                "Indeed",
                "Company Website",
                "Referral",
                "Other"
            ]
        )

        location = c4.text_input(
            "Location / Remote"
        )

        notes = st.text_area(
            "Notes"
        )

        submitted = st.form_submit_button(
            "💾 Save Application"
        )

        if submitted:

            if (
                company.strip()
                and role.strip()
            ):

                add_job_app(
                    company.strip(),
                    role.strip(),
                    source,
                    location.strip(),
                    "Applied",
                    notes.strip()
                )

                st.success(
                    "✅ Application saved successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Company and Role are required."
                )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📈 Analytics":

    st.title(
        "📈 Learning Analytics"
    )

    # --------------------------------------------------------
    # Weekly Progress
    # --------------------------------------------------------

    st.subheader(
        "📅 Weekly Progress"
    )

    weekly = get_weekly_progress()

    if not weekly.empty:

        st.line_chart(
            weekly.set_index("Week")[
                "Progress"
            ]
        )

        st.dataframe(
            weekly,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Weekly progress will appear here."
        )

    # --------------------------------------------------------
    # Monthly Progress
    # --------------------------------------------------------

    st.subheader(
        "🗓️ Monthly Progress"
    )

    monthly = get_monthly_progress()

    if not monthly.empty:

        st.bar_chart(
            monthly.set_index("Month")[
                "Progress"
            ]
        )

        st.dataframe(
            monthly,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Monthly progress will appear here."
        )

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    st.subheader(
        "⚠️ Reset Progress"
    )

    with st.expander(
        "Reset Study Progress"
    ):

        st.warning(
            "This will reset study progress, "
            "interview progress, English progress "
            "and other learning progress. "
            "Job applications should remain preserved."
        )

        confirm = st.checkbox(
            "I understand and want to reset my progress."
        )

        if confirm:

            if st.button(
                "🔄 Reset Study Progress"
            ):

                reset_all_progress()

                st.success(
                    "✅ Study progress has been reset."
                )

                st.rerun()

