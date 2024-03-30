import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

# Load data from CSV file
df = pd.read_csv('data.csv')
# Convert diagnosis column to binary labels (M: 1, B: 0)
df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})
# Drop unnecessary columns (id, Unnamed: 32)
df = df.drop(['id', 'Unnamed: 32'], axis=1)
# Separate features (X) and target (y) columns
X = df.loc[:, df.columns != 'diagnosis']
y = df['diagnosis']

# Split the data into a training set (80%) and a test set (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Construct a pipeline for preprocessing and model training
pipeline = Pipeline([
    ('scaler', StandardScaler()), # Standardize features by removing the mean and scaling to unit variance
    ('pca', PCA(n_components=10)), # Apply Principal Component Analysis for dimensionality reduction
    ('dt', DecisionTreeClassifier()) # Use Decision Tree as the classifier
])

# Define the parameter grid for GridSearchCV
parameters = {
    'dt__max_depth': [None, 10, 20, 30],
    'dt__min_samples_split': [2, 5, 10],
    'dt__min_samples_leaf': [1, 2, 4]
}

# Create a GridSearchCV object with 10-fold cross-validation and recall scoring
grid_search = GridSearchCV(pipeline, parameters, cv=10, scoring='recall')
grid_search.fit(X_train, y_train)

# Display the best parameters found by GridSearchCV
print("Best parameters: ", grid_search.best_params_)
# Extract the best model from GridSearchCV
best_model = grid_search.best_estimator_

# Make predictions on test data
y_pred = best_model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred) * 100
print("Accuracy: {:.2f}%".format(accuracy))

# Calculate precision
precision_B = precision_score(y_test, y_pred, pos_label=0) * 100
precision_M= precision_score(y_test, y_pred, pos_label=1) * 100
print("Precision of Benign class: {:.2f}%".format(precision_B))
print("Precision of Malignant class: {:.2f}%".format(precision_M))

# Calculate recall (sensitivity)
recall_B = recall_score(y_test, y_pred, pos_label=0) * 100
print("Sensitivity of Benign class: {:.2f}%".format(recall_B))
recall_M = recall_score(y_test, y_pred, pos_label=1) * 100
print("Sensitivity of Malignant class: {:.2f}%".format(recall_M))

# Calculate specificity
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
specificity = (tn / (tn + fp)) * 100
print("Specificity: {:.2f}%".format(specificity))

# Calculate F1-score
f1_B = f1_score(y_test, y_pred, pos_label=0) * 100
f1_M = f1_score(y_test, y_pred, pos_label=1) * 100
print("F1-Score of Benign class: {:.2f}%".format(f1_B))
print("F1-Score of Malignant class: {:.2f}%".format(f1_M))

# Calculate ROC curve
y_probs = best_model.predict_proba(X_test)[:, 1]
roc_auc = roc_auc_score(y_test, y_probs) * 100
print("ROC-AUC: {:.2f}%".format(roc_auc))