import pandas as pd

# Load the dataset
df_zomato = pd.read_csv("C:/Users/TARANG/OneDrive/Desktop/zomato/cleaned_zomato.csv")

# Calculate the prior probabilities P(OnlineOrder)
prior_yes = len(df_zomato[df_zomato['online_order'] == 'Yes']) / len(df_zomato)
prior_no = len(df_zomato[df_zomato['online_order'] == 'No']) / len(df_zomato)

# Function to calculate conditional likelihoods P(X|C) dynamically
def calculate_likelihoods(feature, value, outcome):
    subset = df_zomato[df_zomato['online_order'] == outcome]
    return len(subset[subset[feature] == value]) / len(subset)

# Function to get user input for the test instance
def get_user_input():
    print("Please provide the following information:")
    location = input("Enter Location: ").strip()
    rest_type = input("Enter Restaurant Type: ").strip()
    cuisines = input("Enter Cuisines: ").strip()
    listed_in_city = input("Enter Listed City: ").strip()

    return {
        'location': location,
        'rest_type': rest_type,
        'cuisines': cuisines,
        'listed_in(city)': listed_in_city
    }

# Calculate probabilities and predict
def predict_online_order(test_instance):
    # Calculate P(C|X) for online_order = Yes
    prob_yes = prior_yes
    for feature, value in test_instance.items():
        prob_yes *= calculate_likelihoods(feature, value, 'Yes')

    # Calculate P(C|X) for online_order = No
    prob_no = prior_no
    for feature, value in test_instance.items():
        prob_no *= calculate_likelihoods(feature, value, 'No')

    print(f"\nProbability of Yes (Online Order): {prob_yes}")
    print(f"Probability of No (Online Order): {prob_no}")

    if prob_yes > prob_no:
        print("Prediction: Offers Online Order (Yes)")
    else:
        print("Prediction: Does not offer Online Order (No)")

def main():
    test_instance = get_user_input()
    print(f"\nTest Instance: {test_instance}")
    predict_online_order(test_instance)

# Run the program
if __name__ == "__main__":
    main()

