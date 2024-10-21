# Import necessary libraries
import pandas as pd
from sklearn.preprocessing import StandardScaler
import KMedoids  # Updated import
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("C:/Users/TARANG/OneDrive/Desktop/zomato/cleaned_zomato.csv")

# Clean and convert the 'rate' column to float
def clean_and_convert_rate(x):
    if isinstance(x, str):
        x = x.replace('\\n', '').replace('\n', '').strip()  # Remove unwanted characters
        try:
            return float(x.split('/')[0].strip())  # Get the numerical rating
        except ValueError:
            return float('nan')  # Return NaN on error
    return float('nan')  # Return NaN if x is not a string

# Apply the cleaning function to the 'rate' column
df['rate_value'] = df['rate'].apply(clean_and_convert_rate)

# Convert 'approx_cost(for two people)' to numerical
df['approx_cost(for two people)'] = pd.to_numeric(df['approx_cost(for two people)'], errors='coerce')

# Select relevant features for clustering and drop rows with NaN values
features = df[['approx_cost(for two people)', 'rate_value', 'votes']].dropna()

# Check if there are any rows left after dropping NaN values
if features.empty:
    raise ValueError("No valid data available for clustering after cleaning.")

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Apply K-Medoids Clustering
kmedoids = KMedoids(n_clusters=3, random_state=42)
kmedoids.fit(scaled_features)

# Get cluster labels
labels = kmedoids.labels_

# Add the labels to the original dataframe
df['Cluster'] = pd.Series(labels, index=features.index)

# Visualize the clusters (for the first two features)
plt.figure(figsize=(10, 6))
plt.scatter(features['approx_cost(for two people)'], features['rate_value'], c=labels, cmap='viridis', alpha=0.6)
plt.title('K-Medoids Clustering on Zomato Dataset')
plt.xlabel('Approx Cost for Two People')
plt.ylabel('Rating')
plt.colorbar(label='Cluster')
plt.show()
