# Financial-Data-Matching-and-Subset-Sum-Analysis
Reconciling financial amounts between two Excel sheets by implementing both brute force and machine learning approaches.
📌 Project Overview

This project analyzes customer ledger data from an Excel file and computes text similarity using machine learning techniques. The analysis involves data preprocessing, exploratory checks, and feature extraction using TF-IDF, followed by cosine similarity to identify similar records.

The notebook provides a complete workflow for ledger data validation, transformation, and similarity scoring.

✅ Features

Load and process customer ledger data from Excel

Handle missing values and basic data validation

Compute TF-IDF vectors for text-based features

Calculate cosine similarity between ledger entries

Perform exploratory analysis and visualization

📂 Dataset Information

File used: Customer_Ledger_Entries_FULL.xlsx

The dataset contains customer transaction records, which include fields such as:

Customer ID

Document Number

Requirements

Install the required Python packages using:

pip install -r requirements.txt


Main Libraries:

pandas

numpy

matplotlib

scikit-learn

Amount

Description

Other ledger-related attributes


🔍 Key Steps in the Notebook

Data Loading: Import data from Excel using pandas.read_excel()

Data Cleaning: Check for null values, handle missing data

Feature Extraction: Use TfidfVectorizer for text-based fields

Similarity Computation: Calculate cosine similarity using scikit-learn

Visualization: Generate basic plots using matplotlib

📈 Example Use Cases

Detect duplicate or similar ledger entries

Customer behavior analysis based on transaction text

Financial reconciliation using similarity matching

📜 License

This project is licensed under the MIT License.
