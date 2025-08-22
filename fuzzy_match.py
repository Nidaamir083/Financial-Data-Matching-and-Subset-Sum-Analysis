# Install fuzzywuzzy library if you haven't already
%pip install fuzzywuzzy python-Levenshtein

from fuzzywuzzy import fuzz
import time

# Function to calculate fuzzy ratio
def fuzzy_ratio(row):
    return fuzz.ratio(str(row['Description']), str(row['Customer No.']))

# Apply fuzzy matching to the candidates DataFrame
# This might take some time depending on the number of candidates
start_time = time.time()
candidates['Fuzzy_Score'] = candidates.apply(fuzzy_ratio, axis=1)
end_time = time.time()

print(f"Fuzzy matching completed in {end_time - start_time:.2f} seconds.")

# Display the first few rows with the new Fuzzy_Score
display(candidates.head()
