from sklearn import tree
import argparse
import os
import numpy as np
from sklearn.metrics import (accuracy_score,
                             f1_score,
                             roc_auc_score,
                             roc_curve,
                             confusion_matrix,
                             classification_report)
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from azureml.core.run import Run
from azureml.data.dataset_factory import TabularDatasetFactory
from azureml.core import Dataset, Datastore


def clean_data(datos):
    # Rename sales feature into department for better undestanding
    data = datos.rename(columns={"sales": "department"})

    # Map salary into integers
    salary_map = {"low": 0, "medium": 1, "high": 2}
    data["salary"] = data["salary"].map(salary_map)

    # Create dummy variables for department feature
    data = pd.get_dummies(data, columns=["department"], drop_first=True)
    
    # train and test sets: 80/20
    X = data.loc[:, data.columns != "left"].values
    y = data.loc[:, data.columns == "left"].values.flatten()
    return X,y

def main():
    # Add arguments to script
    parser = argparse.ArgumentParser()

    parser.add_argument('--criterion', type=str, default='gini', help= "The function to measure the quality of a split")
    parser.add_argument('--max_depth', type=int, default=None, help= "Maximum depth of the decision tree")
    parser.add_argument('--min_samples_leaf', type=int, default=2, help= "The minimum number of samples required to split an internal node")

    args = parser.parse_args()

    run = Run.get_context()

    run.log("Criterion: ", args.criterion)
    run.log("Max depth:", np.int(args.max_depth))
    run.log("Min samples leaf:", np.int(args.min_samples_leaf))

    ds = TabularDatasetFactory.from_delimited_files(path='https://raw.githubusercontent.com/aiplanethub/Datasets/master/HR_comma_sep.csv')
    
    x, y = clean_data(ds)

    # Split data into train and test sets. Set random state to ensure that we have the same partitions for HyperDrive and AutoML
    # We use the paramenter 'statify=y' to ensure that the proportion of observations of each class are conse
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=123)

    model = tree.DecisionTreeClassifier(criterion=args.criterion, max_depth=args.max_depth, min_samples_leaf=args.min_samples_leaf).fit(x_train, y_train)

    accuracy = accuracy_score(x_test, y_test)
    f1score = f1_score(x_test, y_test)
    auc = roc_auc_score(x_test, y_test, average="weighted")
    run.log("Accuracy ", np.float(accuracy))
    run.log("F1-Score: ", np.float(f1score))
    run.log("Weighted AUC: ", np.float(auc))
    
    model_name = "HyperDrive_model.pkl"
    joblib.dump(model, 'outputs/'+model_name)

if __name__ == '__main__':
    main()

