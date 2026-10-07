import streamlit as st
import csv
import io
from collections import Counter

from regex_parser import parse_log
from dfa import LogDFA
from cfg_validator import validate_log_structure


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Intelligent Log Analyzer",
    page_icon="🔍",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: gray;
    font-size: 18px;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">🔍 Intelligent Log Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Regex + DFA + CFG based Log Analysis System'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

st.markdown("## 📂 Upload Log File")

uploaded_file = st.file_uploader(
    "Upload your .log or .txt file",
    type=["log", "txt"]
)


if uploaded_file is not None:

    # --------------------------------------------------
    # READ FILE
    # --------------------------------------------------

    content = uploaded_file.read().decode("utf-8")

    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]


    # --------------------------------------------------
    # REGEX ANALYSIS
    # --------------------------------------------------

    parsed_logs = []

    for line in lines:

        result = parse_log(line)

        if result:
            parsed_logs.append(result)


    # --------------------------------------------------
    # LOG LEVEL COUNTS
    # --------------------------------------------------

    info_count = 0
    warning_count = 0
    error_count = 0

    for log in parsed_logs:

        level = log.get("level", "").upper()

        if level == "INFO":
            info_count += 1

        elif level == "WARNING":
            warning_count += 1

        elif level == "ERROR":
            error_count += 1


    total_logs = len(parsed_logs)


    # --------------------------------------------------
    # CFG VALIDATION
    # --------------------------------------------------

    valid_count = 0
    invalid_count = 0

    for line in lines:

        try:

            valid = validate_log_structure(line)

            if valid:
                valid_count += 1
            else:
                invalid_count += 1

        except Exception:

            invalid_count += 1


    # --------------------------------------------------
    # DFA STATE TRACKING
    # --------------------------------------------------

    dfa = LogDFA()

    consecutive_errors = 0

    results = []

    suspicious_found = False

    for log in parsed_logs:

        level = log.get("level", "").upper()


        if level == "ERROR":

            consecutive_errors += 1

        else:

            consecutive_errors = 0


        if consecutive_errors == 0:

            state = "S0"

        elif consecutive_errors == 1:

            state = "S1"

        elif consecutive_errors == 2:

            state = "S2"

        else:

            state = "S3"

            suspicious_found = True


        try:
            dfa.process(level)
        except Exception:
            pass


        results.append({
            "Log": log.get("message", ""),
            "Level": level,
            "DFA State": state
        })


    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------

    st.markdown("## 📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📄 Total Logs", total_logs)

    with col2:
        st.metric("ℹ️ INFO", info_count)

    with col3:
        st.metric("⚠️ WARNING", warning_count)

    with col4:
        st.metric("❌ ERROR", error_count)


  



    # --------------------------------------------------
    # CHARTS
    # --------------------------------------------------

    st.markdown("## 📈 Log Level Distribution")

    chart_data = {
        "INFO": info_count,
        "WARNING": warning_count,
        "ERROR": error_count
    }

    st.bar_chart(chart_data)


    st.markdown("## 🔄 DFA State Distribution")

    state_counts = Counter(
        row["DFA State"]
        for row in results
    )

    dfa_chart = {
        "S0": state_counts.get("S0", 0),
        "S1": state_counts.get("S1", 0),
        "S2": state_counts.get("S2", 0),
        "S3": state_counts.get("S3", 0)
    }

    st.bar_chart(dfa_chart)


    # --------------------------------------------------
    # STEP 22
    # SEARCH AND FILTER
    # --------------------------------------------------

    st.markdown("## 🔎 Search & Filter Logs")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        search_text = st.text_input(
            "🔎 Search logs",
            placeholder="Example: database, login, activity..."
        )

    with filter_col2:

        level_filter = st.selectbox(
            "🎚️ Filter by Log Level",
            [
                "ALL",
                "INFO",
                "WARNING",
                "ERROR"
            ]
        )


    # --------------------------------------------------
    # APPLY FILTER
    # --------------------------------------------------

    filtered_results = []

    for row in results:

        message = row["Log"].lower()
        level = row["Level"]

        search_matches = (
            search_text.lower() in message
            if search_text
            else True
        )

        level_matches = (
            level_filter == "ALL"
            or level == level_filter
        )

        if search_matches and level_matches:

            filtered_results.append(row)


    # --------------------------------------------------
    # FILTER RESULT COUNT
    # --------------------------------------------------

    st.info(
        f"🔢 Matching Logs: **{len(filtered_results)}**"
    )


    # --------------------------------------------------
    # FILTERED TABLE
    # --------------------------------------------------

    if filtered_results:

        st.dataframe(
            filtered_results,
            use_container_width=True
        )

    else:

        st.warning(
            "No logs match your search/filter."
        )


    # --------------------------------------------------
    # ALL DFA LOGS
    # --------------------------------------------------

    st.markdown("## 🔄 Complete DFA State Tracking")

    st.dataframe(
        results,
        use_container_width=True
    )


    # --------------------------------------------------
    # FINAL DFA STATE
    # --------------------------------------------------

    if results:

        final_state = results[-1]["DFA State"]

        st.info(
            f"🔵 Final DFA State: **{final_state}**"
        )


    # --------------------------------------------------
    # DFA STATE DIAGRAM
    # --------------------------------------------------

    st.markdown("## 🔷 DFA State Diagram")

    st.components.v1.html("""
    <div style="
        display:flex;
        justify-content:center;
        align-items:center;
        gap:25px;
        font-family:Arial;
        padding:30px;
        background:#f8f9fa;
        border-radius:15px;
    ">

        <div style="
            border:3px solid #2563eb;
            border-radius:50%;
            width:80px;
            height:80px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:bold;
            background:white;
        ">
            S0
        </div>

        <div style="font-size:25px;">→</div>

        <div style="
            border:3px solid #2563eb;
            border-radius:50%;
            width:80px;
            height:80px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:bold;
            background:white;
        ">
            S1
        </div>

        <div style="font-size:25px;">→</div>

        <div style="
            border:3px solid #2563eb;
            border-radius:50%;
            width:80px;
            height:80px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:bold;
            background:white;
        ">
            S2
        </div>

        <div style="font-size:25px;">→</div>

        <div style="
            border:3px solid red;
            border-radius:50%;
            width:80px;
            height:80px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:bold;
            background:#ffe5e5;
        ">
            S3
        </div>

    </div>
    """, height=160)


    # --------------------------------------------------
    # DFA STATE EXPLANATION
    # --------------------------------------------------

    st.markdown("### DFA States")

    st.table({
        "State": ["S0", "S1", "S2", "S3"],
        "Meaning": [
            "No consecutive errors",
            "1 consecutive ERROR",
            "2 consecutive ERRORs",
            "3 or more consecutive ERRORs"
        ]
    })


    # --------------------------------------------------
    # CFG VALIDATION
    # --------------------------------------------------

    st.markdown("## 🧩 CFG Validation")

    cfg_col1, cfg_col2 = st.columns(2)

    with cfg_col1:

        st.metric(
            "✅ Valid Log Structure",
            valid_count
        )

    with cfg_col2:

        st.metric(
            "❌ Invalid Log Structure",
            invalid_count
        )


    # --------------------------------------------------
    # REGEX ANALYSIS
    # --------------------------------------------------

    st.markdown("## 🔎 Regular Expression Analysis")

    regex_rows = []

    for log in parsed_logs:

        regex_rows.append({
            "Date": log.get("date", ""),
            "Time": log.get("time", ""),
            "Level": log.get("level", ""),
            "Message": log.get("message", "")
        })


    if regex_rows:

        st.dataframe(
            regex_rows,
            use_container_width=True
        )


    # --------------------------------------------------
    # CSV REPORT
    # --------------------------------------------------

    st.markdown("## 📥 Download Analysis Report")

    csv_buffer = io.StringIO()

    writer = csv.DictWriter(
        csv_buffer,
        fieldnames=["Log", "Level", "DFA State"]
    )

    writer.writeheader()

    writer.writerows(results)

    csv_data = csv_buffer.getvalue()


    st.download_button(
        label="📥 Download CSV Report",
        data=csv_data,
        file_name="log_analysis_report.csv",
        mime="text/csv"
    )


    # --------------------------------------------------
    # SUCCESS
    # --------------------------------------------------

    st.markdown("---")

    st.success(
        "✅ Log analysis completed successfully!"
    )




    st.info(
        "👆 Upload a .log file to start analyzing your logs."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    "<center>"
    "🔍 Intelligent Log Analyzer | "
    "Regex + DFA + CFG"
    "</center>",
    unsafe_allow_html=True
)