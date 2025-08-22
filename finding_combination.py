# Let's apply the subset sum to a subset of the candidates data
# We'll focus on finding combinations of transactions that match a specific target
# within a small tolerance.

# First, let's select a target from the candidates DataFrame
# For demonstration, let's pick a target with a non-zero remaining amount
target_example = candidates[candidates['Remaining Amount'] != 0].iloc[0]
target_idx = target_example['idx2']
target_amount = target_example['Remaining Amount']

print(f"Selected Target (idx2={target_idx}): Remaining Amount = {target_amount}")

# Now, get all candidate transactions associated with this target
transactions_for_target = candidates[candidates['idx2'] == target_idx]['Amount'].tolist()

print(f"Number of candidate transactions for this target: {len(transactions_for_target)}")
print(f"Candidate transaction amounts: {transactions_for_target[:10]}...") # Print first 10

# We want to find subsets of transactions that sum close to the negative of the target amount
# (since a match would ideally result in a net amount of zero)
# Or, more generally, find subsets that sum to zero when considering both transactions and target amounts.
# Let's use the existing dynamic programming subset sum function (subset_sum_dp)
# For simplicity in using subset_sum_dp which expects positive integers and a positive target,
# let's frame the problem as finding a subset of transactions that sums to the target amount
# or close to it, within a tolerance.
# However, the subset_sum_dp function as implemented finds if a subset *exists* that sums to target,
# not necessarily listing all subsets or handling negative numbers directly.

# To find combinations that sum to a specific target amount (which could be positive or negative),
# and potentially involve both positive and negative transaction amounts,
# we need a subset sum variation that handles this.

# Let's adapt the approach: find subsets of transactions that sum to a value close to the target amount.
# We can try to find subsets that sum to values within a small range around the target amount.

# For this example, let's try to find a subset of positive transaction amounts that sum to the
# absolute value of the target amount within a tolerance, or a subset of all transactions
# (positive and negative) that sum to zero within a tolerance.

# Let's refine the subset sum function or use an alternative if needed for handling signs and tolerance.

# A simpler demonstration with the existing subset_sum_dp would be to find if any subset of
# positive transaction amounts sums to the absolute target amount (if target is positive).

# Let's find positive transaction amounts related to this target
positive_transactions = [abs(amount) for amount in transactions_for_target if amount > 0]
target_abs = abs(target_example['Remaining Amount'])

# Since subset_sum_dp is for positive integers and a positive target, let's scale and round if needed
# and define a reasonable target range.
# This requires careful handling of floating point numbers and potentially large targets.

# A more direct approach for reconciliation might involve finding subsets that sum to a small tolerance around zero.
# This is a variation of the subset sum problem.

# Let's redefine the subset sum problem for this context:
# Given a list of transaction amounts and a target amount, find subsets of transactions
# whose sum, when combined with the target amount, is close to zero.

# Let's try a simpler approach first: find if any single transaction matches the target amount.
# This is already covered by the candidate generation with a small tolerance.

# Let's focus on finding multi-way matches using a subset sum idea.
# Given a target amount, and a list of transaction amounts related to that target,
# find if a subset of these transaction amounts sums to a value that, when added to the target amount, is close to zero.

# Let's try to find subsets of transaction amounts that sum to a value within a tolerance of the target amount's negative.
# target_amount_neg = -target_amount
# tolerance = 1 # Define a tolerance

# We need a subset sum function that can handle a target range and potentially negative numbers in the input list.

# Let's try a brute-force like approach for this small subset of transactions to demonstrate the idea.
# This is not optimized for large numbers of transactions per target.

def find_reconciliation_subsets(transaction_amounts, target_amount, tolerance=1):
    n = len(transaction_amounts)
    solutions = []
    # Iterate through all possible subsets
    for i in range(1, 1 << n): # 1 << n is 2^n
        subset = [transaction_amounts[j] for j in range(n) if (i >> j) & 1]
        if abs(sum(subset) + target_amount) <= tolerance:
            solutions.append(subset)
    return solutions

# Let's apply this to the transactions for the example target
reconciliation_matches = find_reconciliation_subsets(transactions_for_target, target_amount)

print(f"\nSubsets of transactions that reconcile with Target (idx2={target_idx}, Amount={target_amount}):")
if reconciliation_matches:
    for match in reconciliation_matches:
        print(f"  Match found: {match}, Sum: {sum(match)}, Total (with target): {sum(match) + target_amount}")
else:
    print("  No reconciliation subsets found for this target within the tolerance.")

# Note: This brute-force subset finding for each target can still be slow if a target has many candidate transactions.
# For a more efficient solution for many transactions per target, a specialized subset sum
# algorithm that handles sums near zero with floating point numbers and tolerance would be needed.
