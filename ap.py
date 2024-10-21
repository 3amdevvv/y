import pandas as pd
from itertools import combinations


def read_dataset(file_path, nrows=15):
    return pd.read_csv(file_path, nrows=nrows)


def get_transactions(dataset):
    # Select relevant columns for analysis
    relevant_columns = ['location', 'rest_type', 'cuisines', 'online_order']

    # Filtering columns
    return dataset[relevant_columns].apply(lambda row: list(row.dropna().astype(str)), axis=1).tolist()


# Generate candidate itemsets of size k
def generate_candidates(prev_itemsets, k):
    candidates = []
    n = len(prev_itemsets)

    for i in range(n):
        for j in range(i + 1, n):
            itemset1 = prev_itemsets[i]
            itemset2 = prev_itemsets[j]

            if itemset1[:k - 2] == itemset2[:k - 2]:
                candidate = sorted(list(set(itemset1).union(set(itemset2))))

                if candidate not in candidates:
                    candidates.append(candidate)

    return candidates


# Prune itemsets with respect to minimum support
def prune_itemsets(itemsets, transactions, min_support):
    pruned_itemsets = []
    item_counts = {}

    for itemset in itemsets:
        for transaction in transactions:
            if set(itemset).issubset(set(transaction)):
                item_counts[tuple(itemset)] = item_counts.get(tuple(itemset), 0) + 1

    total_transactions = len(transactions)

    for itemset, count in item_counts.items():
        support = count / total_transactions

        if support >= min_support:
            pruned_itemsets.append(list(itemset))

    return pruned_itemsets


# Apriori algorithm
def apriori(dataset, min_support):
    transactions = get_transactions(dataset)
    itemsets = [[item] for item in set(item for transaction in transactions for item in transaction)]
    k = 2
    frequent_itemsets = []

    while itemsets:
        pruned_itemsets = prune_itemsets(itemsets, transactions, min_support)

        if not pruned_itemsets:
            break

        frequent_itemsets.extend(pruned_itemsets)
        itemsets = generate_candidates(pruned_itemsets, k)
        k += 1

    return frequent_itemsets


# Generate association rules
def generate_rules(frequent_itemsets, transactions, min_confidence):
    rules = []
    itemset_support = {}

    # Calculate support
    for itemset in frequent_itemsets:
        support = sum(1 for transaction in transactions if set(itemset).issubset(set(transaction)))
        itemset_support[frozenset(itemset)] = support / len(transactions)

    # Generate rules from the frequent itemsets
    for itemset in frequent_itemsets:
        if len(itemset) > 1:
            itemset = frozenset(itemset)

            for antecedent_size in range(1, len(itemset)):
                for antecedent in combinations(itemset, antecedent_size):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent

                    if antecedent in itemset_support:
                        confidence = itemset_support[itemset] / itemset_support[antecedent]

                        if confidence >= min_confidence:
                            rules.append((set(antecedent), set(consequent), confidence))

    return rules


# Map itemsets to a more readable format
def map_attributes(itemset):
    attribute_map = {
        'Yes': 'Online Order=Yes',
        'No': 'Online Order=No',
        # Add more mappings if needed
    }

    return [attribute_map.get(item, item) for item in itemset]


def percentage_to_fraction(percentage):
    return percentage / 100.0


if __name__ == "__main__":
    file_path = "C:/Users/TARANG/OneDrive/Desktop/zomato/cleaned_zomato.csv"  # Replace with the correct file path
    dataset = read_dataset(file_path, nrows=15)

    min_support = percentage_to_fraction(float(input("Enter the minimum support (as a percentage): ")))
    min_confidence = percentage_to_fraction(float(input("Enter the minimum confidence (as a percentage): ")))

    # Run Apriori algorithm
    frequent_itemsets = apriori(dataset, min_support)

    # Generate association rules
    association_rules = generate_rules(frequent_itemsets, get_transactions(dataset), min_confidence)

    # Output results
    print("\nFrequent Itemsets:")
    for itemset in frequent_itemsets:
        mapped_itemset = map_attributes(itemset)
        print(mapped_itemset)

    print("\nAssociation Rules:")
    for rule in association_rules:
        antecedent, consequent, confidence = rule
        mapped_antecedent = map_attributes(antecedent)
        mapped_consequent = map_attributes(consequent)
        print(f"{mapped_antecedent} => {mapped_consequent}, Confidence: {confidence:.1%}")
