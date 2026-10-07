# 🔍 Intelligent Log Analyzer

An intelligent log analysis system that uses **Regular Expressions (Regex), Deterministic Finite Automata (DFA), and Context-Free Grammar (CFG)** to analyze log files and detect suspicious activities.

---

## 📌 Project Overview

The Intelligent Log Analyzer is a Streamlit-based application designed to analyze system log files.

The system extracts important information from logs, validates their structure, tracks error patterns using DFA, detects suspicious activities, and provides visual reports.

---

## 🎯 Objectives

- Analyze log files automatically
- Extract log information using Regular Expressions
- Validate log structure using Context-Free Grammar
- Track error patterns using DFA
- Detect suspicious consecutive ERROR logs
- Visualize log statistics
- Search and filter logs
- Generate downloadable CSV reports

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Regular Expressions (Regex)
- Deterministic Finite Automata (DFA)
- Context-Free Grammar (CFG)
- CSV
- HTML/CSS

---

## ✨ Features

### 🔎 1. Regular Expression Analysis

Regex is used to extract:

- Date
- Time
- Log level
- Log message

Example:

```text
2026-10-06 10:15:01 INFO User login successful