import mlflow
import pickle

# Set the tracking URI to the same one used in your UI
mlflow.set_tracking_uri("http://127.0.0.1:5001")  

# Create or set the experiment
mlflow.set_experiment("nyc-taxi-experiment")


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    dv, lr = data

    model_name = "Linear Regression"

    with mlflow.start_run(run_name=model_name):
        with open('dict_vectorizer.bin', 'wb') as f_out:
            pickle.dump(dv, f_out)
        mlflow.log_artifact('dict_vectorizer.bin')
        mlflow.sklearn.log_model(lr, 'model')
        mlflow.set_tag("developer","dario")
        mlflow.set_tag("model", "Linear Regression")
    print('OK')
