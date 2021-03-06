import csv
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

from helper import convert_month, convert_types

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Read in file
    df = pd.read_csv('./' + filename + '.csv')
    # Isolate features of dataframe
    X = df.drop('Revenue', axis=1)
    # Convert VisitorType column to numerical values
    X['VisitorType'] = X['VisitorType'].apply(lambda val: 1 if val == 'Returning_Visitor' else 0)
    # Convert month to consistent format
    X['Month'] = X['Month'].apply(lambda val: convert_month(val))
    # Convert Weekend column to numerical values
    X['Weekend'] = X['Weekend'].apply(lambda val: 1 if val == True else 0)
    # Set outcome variable (y)
    y = df['Revenue']
    # Convert predictor and outcome values to lists
    evidence_raw = X.values.tolist()
    labels = y.values.tolist()
    # Ensure types are proper, according to project spec
    evidence = convert_types(evidence_raw)
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Instantiate KNeighbors Classifier and fit to evidence/labels
    return KNeighborsClassifier(n_neighbors=1).fit(evidence,labels)

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Generate a confusion matrix and assign related values
    cm = confusion_matrix(labels, predictions)
    true_negative = cm[0][0]
    false_negative = cm[1][0]
    true_positive = cm[1][1]
    false_positive = cm[0][1]
    # Calculate sensitivity and specificity
    sensitivity = true_positive / (true_positive + false_negative)
    specificity = true_negative / (true_negative + false_positive)
    # Return as tuple
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
