# Create matching keys
sheet1_df["Match_Key"] = sheet1_df["Amount"].astype(str) + "_" + sheet1_df["Description"].astype(str)
sheet2_df["Match_Key"] = sheet2_df["Remaining Amount"].astype(str) + "_" + sheet2_df["Customer No."].astype(str)

# Inner join on Match_Key
matched = pd.merge(sheet1_df, sheet2_df, on="Match_Key", suffixes=("_Sheet1", "_Sheet2"))

# Keep useful columns only
matched = matched[["UID_Sheet1", "Amount", "Description", "UID_Sheet2", "Remaining Amount", "Customer No."]]

# Save Cleaned Data
output_file = "Financial_Data_with_Matches.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    sheet1_df.to_excel(writer, sheet_name="Sheet1", index=False)
    sheet2_df.to_excel(writer, sheet_name="Sheet2", index=False)
    matched.to_excel(writer, sheet_name="Matched_Transactions", index=False)
matched_data = pd.read_excel('/content/Financial_Data_with_Matches.xlsx')
matched_data.head()

from itertools import combinations

def subset_sum_bruteforce(nums, target):
    n = len(nums)
    solutions = []
    
    # Generate all subsets using combinations
    for r in range(1, n+1):
        for subset in combinations(nums, r):
            if sum(subset) == target:
                solutions.append(subset)
    
    return solutions

# Example usage
nums = [3, 34, 4, 12, 5, 2]
target = 9

result = subset_sum_bruteforce(nums, target)
print("All subsets that sum to", target, "are:", result)

def subset_sum_dp(nums, target):
    n = len(nums)
    # DP table: dp[i][j] = True if subset of first i elements can sum to j
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    
    # Sum of 0 is always possible (by choosing empty set)
    for i in range(n + 1):
        dp[i][0] = True
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, target + 1):
            if j < nums[i-1]:
                dp[i][j] = dp[i-1][j]  # cannot include nums[i-1]
            else:
                dp[i][j] = dp[i-1][j] or dp[i-1][j - nums[i-1]]
    
    # Backtrack to find subsets
    solutions = []
    def backtrack(i, j, subset):
        if j == 0:
            solutions.append(tuple(subset))
            return
        if i == 0:
            return
        if dp[i-1][j]:
            backtrack(i-1, j, subset[:])
        if j >= nums[i-1] and dp[i-1][j - nums[i-1]]:
            backtrack(i-1, j - nums[i-1], subset + [nums[i-1]])
    
    if dp[n][target]:
        backtrack(n, target, [])
    
    return solutions

nums = [3, 34, 4, 12, 5, 2]
target = 9

print("Brute Force:", subset_sum_bruteforce(nums, target))
print("Dynamic Programming:", subset_sum_dp(nums, target))

# --- Brute Force Implementation ---
def subset_sum_bruteforce(nums, target):
    n = len(nums)
    solutions = []
    for r in range(1, n+1):
        for subset in combinations(nums, r):
            if sum(subset) == target:
                solutions.append(subset)
    return solutions

# --- Dynamic Programming Implementation ---
def subset_sum_dp(nums, target):
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True
    
    for i in range(1, n + 1):
        for j in range(1, target + 1):
            if j < nums[i-1]:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = dp[i-1][j] or dp[i-1][j - nums[i-1]]
    
    return dp[n][target]

# --- Benchmark Function ---
def benchmark():
    sizes = [10, 15, 20, 25]  # dataset sizes to test
    target = 50
    
    results = []
    for n in sizes:
        nums = [random.randint(1, 20) for _ in range(n)]
        
        # Brute Force Timing
        start = time.time()
        subset_sum_bruteforce(nums, target)
        brute_time = time.time() - start
        
        # DP Timing
        start = time.time()
        subset_sum_dp(nums, target)
        dp_time = time.time() - start
        
        results.append((n, round(brute_time, 5), round(dp_time, 5)))
    
    return results

# Run benchmark
results = benchmark()

# Display results
print(" Dataset Size | Brute Force (sec) | DP (sec)")
print("--------------|-------------------|----------")
for n, brute, dp in results:
    print(f"{n:12} | {brute:17} | {dp:8}")

# Split results for plotting
sizes = [r[0] for r in results]
brute_times = [r[1] for r in results]
dp_times = [r[2] for r in results]

# --- Plot 1: Normal Scale ---
plt.figure(figsize=(8,5))
plt.plot(sizes, brute_times, marker="o", label="Brute Force (Exponential)")
plt.plot(sizes, dp_times, marker="s", label="Dynamic Programming (Polynomial)")
plt.xlabel("Dataset Size (n)")
plt.ylabel("Execution Time (seconds)")
plt.title("Subset Sum Problem: Brute Force vs DP (Normal Scale)")
plt.legend()
plt.grid(True)
plt.show()

# --- Plot 2: Logarithmic Y-Axis ---
plt.figure(figsize=(8,5))
plt.plot(sizes, brute_times, marker="o", label="Brute Force (Exponential)")
plt.plot(sizes, dp_times, marker="s", label="Dynamic Programming (Polynomial)")
plt.xlabel("Dataset Size (n)")
plt.ylabel("Execution Time (seconds, log scale)")
plt.title("Subset Sum Problem: Brute Force vs DP (Log Scale)")
plt.yscale("log")
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()

