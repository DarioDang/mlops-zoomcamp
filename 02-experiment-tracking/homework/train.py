import os
import pickle
import click
import mlflow 
import mlflow.sklearn


from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Set the tracking URI to the same one used in your UI
mlflow.set_tracking_uri("http://127.0.0.1:5002")  

# Create or set the experiment
mlflow.set_experiment("nyc-taxi-experiment")

# Enable autologging
mlflow.sklearn.autolog()

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))
    
    #Run the MLFlow
    with mlflow.start_run(run_name="RandomForest"):
        mlflow.set_tag("developer","Dario")
        mlflow.set_tag("model", "RandomForest")
        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)
        
        # Calculate RMSE
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        
        # Show the result 
        print(f"RMSE: {rmse:.4f}")


if __name__ == '__main__':
    run_train()