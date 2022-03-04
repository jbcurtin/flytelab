"""
Hello World
------------
This simple workflow calls a task that returns "Hello World" and then just sets that as the final output of the workflow.
"""
import time
import typing
from typing import Any, Dict, List, Tuple
from datetime import datetime

from flytekit import task, workflow
from pandas import pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble.forest import RandomForestClassifier

# from tasks import modeling


DELAY = 10

@task
def load_data(*, primary_data: str) -> pd.Dataframe:
    
    return pd.read_csv(primary_data)

@task
def create_features(*, data: pd.Dataframe) -> pd.Dataframe:
    time.sleep(DELAY)
    return data

@task
def split_data(*, data: pd.Dataframe) -> Tuple[pd.Dataframe, pd.Dataframe]:
    X_train, X_val, y_train, y_val = train_test_split(
        data.drop('label', axis=1),
        data['label'],
        test_size=0.2,
        random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(
        X_val,
        y_val,
        test_size=0.2,
        random_state=42)
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)

def train_model(*, train_data, val_data) -> Any:
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(train_data[0], train_data[1])
    return rf

def validate_model(*, model: Any, test_data: pd.Dataframe) -> Any:
    pred = model.predict(test_data[0])
    scores = model.score(test_data[1], pred)
    return scores

@workflow
def model_training(*, primary_data: str) -> Tuple[Any, dict]:
    data = load_data(primary_data = primary_data)
    features = create_features(data = data)
    train, val, test = split_data(data = features)
    model = train_model(train_data = train, val_data = val)
    scores = validate_model(model = model, test_data = test)
    return model, scores

if __name__ == "__main__":
    print('Running Model Training Workflow')
    print(f"Results: { model_training(primary_data=primary_data) }")
