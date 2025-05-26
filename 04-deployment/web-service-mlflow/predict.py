import pickle 
import mlflow
import os 
from mlflow.tracking import MlflowClient
from flask import Flask, request, jsonify


#MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000/'
#mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


# RUN_ID = '33d91be4d8184963b8648d4419ef6507' 
RUN_ID = os.getenv('RUN_ID')

logged_model = f'mlartifacts/1/{RUN_ID}/artifacts/model'
#logged_model = f'runs:/{RUN_ID}/model'

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