import pandas as pd
import numpy as np

df = pd.read_excel('/content/Customer_Ledger_Entries_FULL.xlsx')
df.head()

# Select the 'Description' and 'Amount' columns and create a copy
Transactions = df[['Description', 'Amount']].copy()

# Save the selected columns to a new Excel file
Transactions.to_excel('Sheet1.xlsx', index=False)

print("Sheet1.xlsx file created successfully.")

# Select the 'Customer No' and 'Remaining Amount' columns and create a copy
Targets = df[['Customer No.', 'Remaining Amount']].copy()

# Save the selected columns to a new Excel file
Targets.to_excel('Sheet2.xlsx', index=False)

print("Sheet2.xlsx file created successfully.")

# Read the Sheet1.xlsx file into a pandas DataFrame
sheet1_df = pd.read_excel('Sheet1.xlsx')

# Display the content of the DataFrame
print("Content of Sheet1.xlsx:")
display(sheet1_df.head())

sheet2_df = pd.read_excel('Sheet2.xlsx')

# Display the content of the DataFrame
print("Content of Sheet2.xlsx:")
display(sheet2_df.head())

#  Handle Missing Values
sheet1_df["Amount"].fillna(0, inplace=True)
sheet1_df["Description"].fillna("Unknown", inplace=True)

sheet2_df["Remaining Amount"].fillna(0, inplace=True)
sheet2_df["Customer No."].fillna("Unknown", inplace=True)

# Drop rows if both columns are missing/empty
sheet1_df = sheet1_df[(sheet1_df["Amount"] != 0) | (sheet1_df["Description"] != "Unknown")]
sheet2_df = sheet2_df[(sheet2_df["Remaining Amount"] != 0) | (sheet2_df["Customer No."] != "Unknown")]

# Standardize Amount Formats

def clean_amount(x):
    if isinstance(x, str):
        # Remove currency symbols and commas
        x = x.replace("$", "").replace("€", "").replace("₹", "").replace(",", "")
    try:
        return round(float(x), 2)
    except:
        return 0.00

sheet1_df["Amount"] = sheet1_df["Amount"].apply(clean_amount)
sheet2_df["Remaining Amount"] = sheet2_df["Remaining Amount"].apply(clean_amount)

# Create Unique Identifiers
sheet1_df["UID"] = ["S1_" + str(i) for i in range(1, len(sheet1_df)+1)]
sheet2_df["UID"] = ["S2_" + str(i) for i in range(1, len(sheet2_df)+1)]

# Save Cleaned Data
output_file = "Processed_Financial_Data_Cleaned.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    sheet1_df.to_excel(writer, sheet_name="Sheet1", index=False)
    sheet2_df.to_excel(writer, sheet_name="Sheet2", index=False)
cleaned_data = pd.read_excel('/content/Processed_Financial_Data_Cleaned.xlsx')
cleaned_data.head()


