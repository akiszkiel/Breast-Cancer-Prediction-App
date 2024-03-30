import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
import joblib
from sklearn.pipeline import Pipeline

def train_model():
    """
    Train the machine learning model using Logistic Regression with PCA.
    
    Returns:
        best_model: trained model with best parameters
        X_test: test features
        y_test: test labels
    """
    # Load data from CSV file
    df = pd.read_csv('data.csv')

    # Convert diagnosis column to binary labels (M: 1, B: 0)
    df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})

    # Drop unnecessary columns (id, Unnamed: 32)
    df = df.drop(['id', 'Unnamed: 32'],  axis=1)  

    # Separate features (X) and target (y) columns
    X = df.loc[:, df.columns != 'diagnosis']  # Exclude "diagnosis" from features
    y = df['diagnosis']  

    # Split the data into a training set (80%) and a test set (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Construct a pipeline for preprocessing and model training
    pipeline = Pipeline([
        ('scaler', StandardScaler()), # Standardize features by removing the mean and scaling to unit variance
        ('pca', PCA(n_components=10)), # Apply Principal Component Analysis for dimensionality reduction
        ('logreg', LogisticRegression()) # Use Logistic Regression as the classifier
    ])

    # Define the parameter grid for GridSearchCV
    parameters = {
        'logreg__C': [0.01, 0.1, 1, 10, 100],
        'logreg__penalty': ['l2']  # 'l1' można użyć z solverem 'liblinear'
    }

    # Create a GridSearchCV object with 10-fold cross-validation and recall scoring
    grid_search = GridSearchCV(pipeline, parameters, cv=10, scoring='recall')
    grid_search.fit(X_train, y_train)

    # Display the best parameters found by GridSearchCV
    # print("Best parameters: ", grid_search.best_params_)

    # Extract the best model from GridSearchCV
    best_model = grid_search.best_estimator_

    return best_model, X_test, y_test

def save_model(reg_model, X_test, y_test, file_path='trained_model.joblib'):
    """
    Save the trained model along with test data to a file.
    
    Args:
        reg_model: trained model
        X_test: test features
        y_test: test labels
        file_path: path to save the model file
    """
    joblib.dump((reg_model, X_test, y_test), file_path)

    
def load_model(file_path='trained_model.joblib'):
    """
    Load the trained model and test data from a file.
    
    Args:
        file_path: path to the saved model file
    
    Returns:
        reg_model: trained model
        X_test: test features
        y_test: test labels
    """
    return joblib.load(file_path)


def evaluate_model(X_test, y_test, reg_model):
    """
    Evaluate the trained model on test data and display performance metrics.
    
    Args:
        X_test: test features
        y_test: test labels
        reg_model: trained model
    
    Returns:
        Tuple containing various performance metrics
    """

    # Make predictions on test data
    y_pred = reg_model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred) * 100
    print("Accuracy: {:.2f}%".format(accuracy))

    # Calculate precision
    precision_B = precision_score(y_test, y_pred, pos_label=0) * 100
    precision_M= precision_score(y_test, y_pred, pos_label=1) * 100
    print("Precision of Benign class: {:.2f}%".format(precision_B))
    print("Precision of Malignant class: {:.2f}%".format(precision_M))

    # Calculate recall (sensitivity)
    recall_M = recall_score(y_test, y_pred, pos_label=1) * 100
    print("Sensitivity of Malignant class: {:.2f}%".format(recall_M))

    # Calculate and print specificity
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    specificity = (tn / (tn + fp)) * 100
    print("Specificity: {:.2f}%".format(specificity))

    # Calculate and print F1-score
    f1_B = f1_score(y_test, y_pred, pos_label=0) * 100
    f1_M = f1_score(y_test, y_pred, pos_label=1) * 100
    print("F1-Score of Benign class: {:.2f}%".format(f1_B))
    print("F1-Score of Malignant class: {:.2f}%".format(f1_M))

    # Calculate ROC curve
    y_probs = reg_model.predict_proba(X_test)[:, 1]
    roc_auc = roc_auc_score(y_test, y_probs) * 100
    print("ROC-AUC: {:.2f}%".format(roc_auc))

    return accuracy, precision_M, precision_B, recall_M, specificity, f1_M, f1_B, roc_auc

if __name__ == "__main__":
    # Train the model and save it
    reg_model, X_test, y_test = train_model()
    save_model(reg_model, X_test, y_test)

