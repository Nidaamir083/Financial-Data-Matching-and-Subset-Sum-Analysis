import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# --- Load data ---
sheet1_df = pd.read_excel("/content/Sheet1.xlsx")
sheet2_df = pd.read_excel("/content/Sheet2.xlsx")

# Reset index
sheet1_df = sheet1_df.reset_index().rename(columns={"index": "idx1"})
sheet2_df = sheet2_df.reset_index().rename(columns={"index": "idx2"})

# --- Candidate generation (filter to reduce size) ---
# Only keep pairs with amounts within ±50
candidates = (
    sheet1_df.assign(key=1)
    .merge(sheet2_df.assign(key=1), on="key")
    .drop("key", axis=1)
)
candidates = candidates[
    (candidates["Amount"] - candidates["Remaining Amount"]).abs() <= 50
]

print(f"Candidate pairs reduced to: {len(candidates)}")

# --- TF-IDF similarity (only on candidates, not full cross) ---
tfidf = TfidfVectorizer().fit(
    sheet1_df["Description"].astype(str).tolist()
    + sheet2_df["Customer No."].astype(str).tolist()
)

desc_vecs = tfidf.transform(candidates["Description"].astype(str))
cust_vecs = tfidf.transform(candidates["Customer No."].astype(str))
candidates["Text_Similarity"] = [
    cosine_similarity(desc_vecs[i], cust_vecs[i])[0, 0] for i in range(len(candidates))
]

# --- Feature Engineering ---
candidates["Amount_Diff"] = (candidates["Amount"] - candidates["Remaining Amount"]).abs()
candidates["Exact_Match"] = (candidates["Amount"] == candidates["Remaining Amount"]).astype(int)

# --- Synthetic Labels ---
# Create synthetic labels based on a threshold for Amount_Diff and Text_Similarity
candidates["Match_Label"] = (
    (candidates["Amount_Diff"] < 1) & (candidates["Text_Similarity"] > 0.7)
).astype(int)

# --- Train ML model ---
X = candidates[["Amount_Diff", "Exact_Match", "Text_Similarity"]]
y = candidates["Match_Label"]

# Check if there are any positive labels before splitting
if y.sum() == 0:
    print("No positive matches generated with the current synthetic labeling criteria.")
else:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)

    print("=== Random Forest Results ===")
    print(classification_report(y_test, clf.predict(X_test)))
    print("ROC AUC:", roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1]))
