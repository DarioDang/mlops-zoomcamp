import pickle 
import mlflow
from mlflow.tracking import MlflowClient
from flask import Flask, request, jsonify


MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000/'
RUN_ID = '25c0958b9a03453eb4ec695278c383f5'

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

path = client.download_artifacts(run_id = RUN_ID, path='dict_vectorizer.bin')
print(f'downloading the dict vectorizer to {path}')

with open(path, 'rb') as f_out:
    dv = pickle.load(f_out)

logged_model = f'runs:/{RUN_ID}/model'

# Load model as a PyFuncModel.
model = mlflow.pyfunc.load_model(logged_model)


# Define prepare function
def prepare_features(ride):
    "Write a function to prepare the features"
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

# Define predict function
def predict(features):
   "Write a function to predict"
   preds = model.predict([features])
   return preds[0]


app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
# Define endpoint function
def predict_endpoint():
   "Write a endpoint function"
   ride = request.get_json()
   features = prepare_features(ride)
   pred = predict(features)

   results = {
      'duration': pred,
      'model_version': RUN_ID,
   }

   return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)