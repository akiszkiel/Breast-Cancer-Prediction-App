import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load data from CSV file
df = pd.read_csv('data.csv')  

# Drop unnecessary columns (id, diagnosis, Unnamed: 32)
X = df.drop(['id', 'diagnosis', 'Unnamed: 32'], axis=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X) # Standardize features by removing the mean and scaling to unit variance

# Initialize PCA object for dimensionality reduction
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

# Calculate the eigenvalues
eigenvalues = pca.explained_variance_

# Plot eigenvalues to visualize the variance explained by each principal component
plt.plot(range(1, len(eigenvalues) + 1), eigenvalues, marker='o')
plt.xlabel('Liczba komponentów')
plt.ylabel('Wartości własne')
plt.title('Wykres osypiska')
plt.grid()
plt.show()

# Calculate cumulative explained variance ratio to assess the cumulative contribution of principal components
explained_variance = pca.explained_variance_ratio_.cumsum()

# Plot cumulative explained variance to determine the optimal number of principal components
plt.plot(range(1, len(explained_variance) + 1), explained_variance, marker='o', linestyle='-')
plt.xlabel('Liczba komponentów')
plt.ylabel('Wyjaśniona wariancja')
plt.title('Całkowita wyjaśniona wariancja')
plt.axhline(y=0.95, color = 'r', linestyle = '--')
plt.grid()
plt.show()

