import pickle 

from flask import Flask, request, jsonify

with open('lin_reg.bin', 'rb') as f_in:
   (dv,  model) = pickle.load(f_in)

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
   X = dv.transform(features)
   preds = model.predict(X)
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
      'duration': pred
   }

   return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)