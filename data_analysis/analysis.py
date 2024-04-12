import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, shapiro
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde

df = pd.read_csv('data.csv')
df = df.drop(['id','Unnamed: 32'],axis=1)

# Calculate the number of rows and columns in the dataset
print("Total data points",df.shape[0])
print("Total number of features: ", df.shape[1])

# Check for missing values in the dataset
null_values = df.isnull().values.any()
if null_values == True:
    print("There are some missing values in data")
else:
    print("There are no missing values in the dataset")

data_counts = df['diagnosis'].value_counts()

# Calculate the percentages of Malignant and Benign diagnoses
percent_malignant = (data_counts['M'] / len(df)) * 100
percent_benign = (data_counts['B'] / len(df)) * 100

# Display the counts and percentages
print(f"Malignant (M): {percent_malignant:.2f}%")
print(f"Benign (B): {percent_benign:.2f}%")

# Create a bar plot showing the distribution of diagnoses
plt.bar(data_counts.index, data_counts)
plt.ylabel("Number of observations")
plt.title("Diagnosis")
plt.xticks(data_counts.index, data_counts.index)  
plt.show()

# Calculate the correlation matrix for features
features_df = df.drop('diagnosis', axis=1)
correlation_matrix = features_df.corr()

# Plot the heatmap of the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, vmin=-1, vmax=1, annot_kws={"size": 5})
plt.tick_params(axis='both', which='major', labelsize=5)
plt.title("Heatmap of Correlation Matrix")
plt.show()

# Initialize counters for different correlation categories
count_moderate = 0
count_strong = 0
count_very_strong = 0

# Iterate through the correlation matrix columns
for i in range(correlation_matrix.shape[0]):
    for j in range(i+1, correlation_matrix.shape[1]):
        correlation = correlation_matrix.iloc[i, j]
        if 0.4 <= abs(correlation) < 0.7:
            count_moderate += 1
        elif 0.7 <= abs(correlation) < 0.9:
            count_strong += 1
        elif abs(correlation) >= 0.9:
            count_very_strong += 1

# Calculate the total number of possible feature pairs
total_pairs = (correlation_matrix.shape[0] * (correlation_matrix.shape[0] - 1)) / 2

# Calculate the percentage of feature pairs in each correlation category
percent_moderate = (count_moderate / total_pairs) * 100
percent_strong = (count_strong / total_pairs) * 100
percent_very_strong = (count_very_strong / total_pairs) * 100

print("\nPercentage of feature pairs in different correlation categories:")
print("Moderate correlations:", percent_moderate)
print("Strong correlations:", percent_strong)
print("Very strong correlations:", percent_very_strong)

# Define a function to calculate the overlap percentage between two density plots
def calculate_overlap_mc(x_malignant, y_malignant, x_benign, y_benign, num_samples=10000):
    # Calculate the boundaries of overlapping curves
    min_x = max(min(x_malignant), min(x_benign))
    max_x = min(max(x_malignant), max(x_benign))
    min_y = max(min(y_malignant), min(y_benign))
    max_y = min(max(y_malignant), max(y_benign))

    # Initialize the counter for points in the overlapping area
    overlap_count = 0

    # Randomly sample points and check if they fall within the overlapping area of the curves
    for _ in range(num_samples):
        x_sample = np.random.uniform(min_x, max_x)
        y_sample_malignant = np.interp(x_sample, x_malignant, y_malignant)
        y_sample_benign = np.interp(x_sample, x_benign, y_benign)

        if min_y <= y_sample_malignant <= max_y and min_y <= y_sample_benign <= max_y:
            overlap_count += 1

    # Calculate the percentage overlap of the curves
    overlap_percentage = (overlap_count / num_samples) * 100

    return overlap_percentage

# Iterate through features and perform various analyses
features = features_df.columns
for feature in features:
    selected_feature = df[feature]
    

    # Calculate mean, standard deviation, median, skewness, kurtosis
    mean = selected_feature.mean()
    std_dev = selected_feature.std()
    median = selected_feature.median()
    skewness = skew(selected_feature)
    kurt = kurtosis(selected_feature)

    print(f"Mean of {feature}: {mean}")
    print(f"Standard Deviation of {feature}: {std_dev}")
    print(f"Median of {feature}: {median}\n")
    print(f"Skewness of {feature}: {skewness}")
    print(f"Kurtosis of {feature}: {kurt}\n")
    
    # Create a histogram with a density plot
    sns.histplot(selected_feature, bins=10, kde=True, color='blue', label='Histogram')
    plt.axvline(mean, color='green', label=f'Mean: {mean:.2f}')
    plt.axvline(median, color='red',  label=f'Median: {median:.2f}')
    plt.title(f'Histogram of {feature}')
    plt.xlabel(feature)
    plt.ylabel('Number of observations')
    sns.kdeplot(selected_feature, color='blue', label='Density plot', legend=True)
    legend = plt.legend()
    plt.show()

    # Create a boxplot
    plt.figure(figsize=(6, 4))
    sns.boxplot(x='diagnosis', y=selected_feature, data=df, palette=['red', 'green'], hue='diagnosis', legend=False)
    plt.title(f'Boxplot of {feature}')
    plt.xlabel('Diagnosis (M: Malignant, B: Benign)')
    plt.ylabel(feature)
    plt.show()


    # Create a density plot for the Malignant and Benign 
    plt.figure(figsize=(8, 6))
    sns.kdeplot(df[df['diagnosis'] == 'M'][feature], color='red', label='Malignant')
    sns.kdeplot(df[df['diagnosis'] == 'B'][feature], color='green', label='Benign')
    plt.title(f'Density Plot for {feature}')
    plt.xlabel(feature)
    plt.ylabel('Density')
    plt.legend()
    plt.show()

    selected_feature_malignant = df[df['diagnosis'] == 'M'][feature]
    selected_feature_benign = df[df['diagnosis'] == 'B'][feature]

    # Generate x and y vectors for both classes
    kde_malignant = gaussian_kde(selected_feature_malignant)
    kde_benign = gaussian_kde(selected_feature_benign)
    
    x_values = np.linspace(min(selected_feature_malignant.min(), selected_feature_benign.min()),
                           max(selected_feature_malignant.max(), selected_feature_benign.max()), 1000)
    
    y_values_malignant = kde_malignant(x_values)
    y_values_benign = kde_benign(x_values)
    
    # Calculate overlap percentage of density plots
    overlap_percentage = calculate_overlap_mc(x_values, y_values_malignant, x_values, y_values_benign)
    print(f"Percentage overlap between Malignant and Benign density plots for {feature}: {overlap_percentage:.2f}%")

    # Perform Shapiro-Wilk test
    stat, p = shapiro(selected_feature)
    print(f"Shapiro-Wilk test for {feature}:")
    print(f" Test Statistic: {stat}")
    print(f" P-Value: {p}")
    
    if p < 0.05:
        print("  The data does not follow a normal distribution.\n")
    else:
        print("  The data follows a normal distribution.\n")

    # Count outliers based on IQR method
    Q1 = selected_feature.quantile(0.25)
    Q3 = selected_feature.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    print(f"{feature}: Lower Bound (IQR) = {lower_bound:.4f}, Upper Bound (IQR) = {upper_bound:.4f}")
    outliers = (selected_feature < lower_bound) | (selected_feature > upper_bound)
    outliers_count = outliers.sum()
    print(f"Number of outliers in {feature}: {outliers_count}\n")

    # Calculate lower and upper percentiles
    lower_percentile = selected_feature.quantile(0.01)
    upper_percentile = selected_feature.quantile(0.99)

    # Count outliers based on the lower and upper percentiles
    count = ((selected_feature < lower_percentile) | (selected_feature > upper_percentile)).sum()

    print(f"{feature}: Lower Bound (1st percentile) = {lower_percentile:.4f}, Upper Bound (99th percentile) = {upper_percentile:.4f}")
    print(f"Number of outliers in {feature}: {count}\n")

