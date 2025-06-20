import requests 
import json 

from deepdiff import DeepDiff

with open('event.json', 'rt', ecoding='utf-8') as f_in:
    event = json.load(f_in)



url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
actual_response = requests.post(url, json=event)
print('actual_response: ')
print(json.dumps(actual_response.json(), indent=2))
expected_response = {
    'predictions': [{
        'model': 'ride_duration_prediction_model', 
        'version': '3ec150b70a5549769f4acd9bc09da04b', 
        'prediction': {
            'ride_duration': 18.18, 
            'ride_id': 256
        }
    }]}
#print(response.json())

diff  = DeepDiff(actual_response.json(), expected_response, significant_digits= 1)
print(f'diff= {diff}')

assert 'type_changes' not in diff 
assert 'value_changes' not in diff