# 🛡️ PhishGuard AI

## AI-Powered URL Phishing Detection Using Machine Learning, Deep Learning, and an Expert System

PhishGuard AI is a web-based phishing URL detection system that analyzes a submitted URL using three complementary approaches:

1. **Machine Learning** using Random Forest
2. **Deep Learning** using a Feed-Forward Artificial Neural Network (ANN)
3. **Rule-Based Expert System** using security-oriented URL indicators

The system combines the outputs of these components into a single risk score from **0 to 100** and classifies the URL as either:

- `legitimate`
- `potentially_phishing`

> ⚠️ **Important:** PhishGuard AI performs **static URL-string analysis only**. Submitted URLs are not visited, fetched, crawled, or opened by the application.

---

# 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Objectives](#-objectives)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [How Detection Works](#-how-detection-works)
- [Feature Extraction](#-feature-extraction)
- [Machine Learning Model](#-machine-learning-model)
- [Deep Learning Model](#-deep-learning-model)
- [Expert Rule System](#-expert-rule-system)
- [Risk Score Calculation](#-risk-score-calculation)
- [Dataset](#-dataset)
- [Model Evaluation](#-model-evaluation)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Running Locally](#-running-locally)
- [Running with Docker](#-running-with-docker)
- [Testing](#-testing)
- [Example Prediction](#-example-prediction)
- [AIES Concepts Demonstrated](#-aies-concepts-demonstrated)
- [Security and Privacy](#-security-and-privacy)
- [Limitations](#-limitations)
- [Future Scope](#-future-scope)
- [Conclusion](#-conclusion)

---

# 🎯 Problem Statement

Phishing attacks frequently use deceptive URLs to trick users into visiting malicious websites or revealing sensitive information.

Traditional URL inspection can be difficult for users because suspicious URLs may contain subtle structural characteristics such as:

- Unusually long URLs
- Excessive digits
- Multiple subdirectories
- Suspicious keywords
- IP addresses instead of domain names
- URL shortening services
- Suspicious encoding
- Account, login, verification, or security-related terminology

PhishGuard AI addresses this problem by automatically analyzing URL characteristics and combining Machine Learning, Deep Learning, and expert rules to provide an interpretable phishing-risk assessment.

---

# 🎯 Objectives

The main objectives of PhishGuard AI are:

- Analyze URLs without visiting or fetching them.
- Extract meaningful structural and lexical URL features.
- Detect potentially phishing URLs using Machine Learning.
- Detect potentially phishing URLs using Deep Learning.
- Apply expert security rules to identify suspicious URL indicators.
- Combine ML, DL, and expert-system information into a unified risk score.
- Provide an easy-to-use web interface.
- Store prediction history locally using SQLite.
- Provide reproducible testing and Docker-based deployment.

---

# ✨ Key Features

### 🔍 URL Analysis

Users can submit an HTTP or HTTPS URL for analysis.

### 🧠 Machine Learning

A Random Forest classifier analyzes 27 URL features.

### 🤖 Deep Learning

A feed-forward Artificial Neural Network analyzes the same 27-feature representation after scaling.

### 📋 Expert System

A rule-based system identifies explicit suspicious URL indicators.

### 📊 Risk Score

The system produces a final score from 0 to 100.

### 🗂️ Prediction History

Previous predictions are stored in a SQLite database.

### 🌐 Web Interface

The React frontend provides:

- URL input
- Prediction result
- Risk score
- ML probability
- DL probability
- Expert indicators
- Recent prediction history

### 🐳 Docker Deployment

The application can run as a multi-container system using Docker Compose.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         └──────────┬──────────┘
                                    │
                                    │ Submit URL
                                    ▼
                         ┌─────────────────────┐
                         │   React Frontend    │
                         │   Vite + Nginx      │
                         └──────────┬──────────┘
                                    │
                                    │ /api/predict
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend   │
                         └──────────┬──────────┘
                                    │
                              URL Validation
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Shared Feature     │
                         │     Extractor       │
                         │     27 Features     │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐       ┌──────────────┐
       │   Random    │       │     ANN     │       │    Expert    │
       │   Forest    │       │ Deep Learn. │       │ Rule System  │
       └──────┬──────┘       └──────┬──────┘       └──────┬───────┘
              │                     │                     │
              │ ML Probability      │ DL Probability     │ Indicators
              └─────────────────────┼─────────────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │    Risk Engine      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Final Classification│
                         │    + Risk Score     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ SQLite Prediction   │
                         │      History        │
                         └─────────────────────┘
