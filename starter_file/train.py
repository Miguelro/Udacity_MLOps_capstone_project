from sklearn.linear_model import LogisticRegression
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
    
    data = datos.to_pandas_dataframe().dropna()

    # Map salary into integers
    salary_map = {"low": 0, "medium": 1, "high": 2}
    data["salary"] = data["salary"].map(salary_map)

    # Create dummy variables for department feature
    dept = pd.get_dummies(data.Department, prefix="dept")
    data.drop("Department",inplace=True,axis=1) 
    data = data.join(dept)
    # train and test sets: 80/20
    X = data.loc[:, data.columns != "left"].values
    y = data.loc[:, data.columns == "left"].values.flatten()
    return X,y

def main():
    # Add arguments to script
    parser = argparse.ArgumentParser()

    parser.add_argument('--C', type=float, default=1.0, help="Inverse of regularization strength. Smaller values cause stronger regularization")
    parser.add_argument('--max_iter', type=int, default=100, help="Maximum number of iterations to converge")

    args = parser.parse_args()

    run = Run.get_context()

    run.log("Regularization Strength:", np.float(args.C))
    run.log("Max iterations:", np.int(args.max_iter))

    # Create TabularDataset using TabularDatasetFactory
    # Data is located at:
    # 'https://raw.githubusercontent.com/aiplanethub/Datasets/master/HR_comma_sep.csv'
    

    #ds = ### YOUR CODE HERE ###
    ds = TabularDatasetFactory.from_delimited_files(path='https://raw.githubusercontent.com/aiplanethub/Datasets/master/HR_comma_sep.csv')
    
    x, y = clean_data(ds)

    # Split data into train and test sets. Set random state to ensure that we have the same partitions for HyperDrive and AutoML
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

    model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)
    run.log("Accuracy ", np.float(accuracy))

    model_name = "HyperDrive_model.pkl"
    joblib.dump(model, 'outputs/'+model_name)

if __name__ == '__main__':
    main()

