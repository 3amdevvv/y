# Import necessary librarie


# Import necessary libraries
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = pd.read_csv("C:/Users/TARANG/OneDrive/Desktop/zomato/cleaned_zomato.csv")

# Display the first few rows of the dataset
print("Initial DataFrame:\n", df.head())

# Data Preprocessing
# Select relevant features for clustering
# Adjust the feature names according to your dataset.
features = df[['approx_cost(for two people)', 'rate', 'votes']].copy()

# Clean and convert the 'rate' column to numeric
def clean_and_convert_rate(x):
    if isinstance(x, str):
        # Remove unwanted characters
        x = x.replace('\\n', '').replace('\n', '').strip()
        try:
            return float(x.split('/')[0])  # Take the first part before '/'
        except ValueError:
            return float('nan')  # Return NaN if conversion fails
    return float('nan')  # Return NaN if x is not a string

# Apply the cleaning function
features['rate'] = features['rate'].apply(clean_and_convert_rate)

# Convert 'approx_cost(for two people)' to numeric
features['approx_cost(for two people)'] = pd.to_numeric(features['approx_cost(for two people)'], errors='coerce')

# Drop rows with NaN values
features.dropna(inplace=True)

# Standardize the features if necessary
# Scaling is often important for clustering algorithms
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Perform Single Linkage Agglomerative Clustering
linked = linkage(scaled_features, method='single')

# Plotting the Dendrogram
plt.figure(figsize=(10, 7))
dendrogram(linked, orientation='top', labels=list(range(len(features))), distance_sort='descending', show_leaf_counts=True)
plt.title('Dendrogram for Single Linkage Agglomerative Clustering')
plt.xlabel('Sample Index')
plt.ylabel('Distance')
plt.show()
