import os 
import boto3
import json
from pprint import pprint
from deepdiff import DeepDiff

# Configure the endpoint using boto3
kinesis_endpoint = os.getenv('KINESIS_ENDPOINT_URL', "http://localhost:4566")
kinesis_client = boto3.client('kinesis', endpoint_url=kinesis_endpoint)

stream_name = os.getenv('PREDICTIONS_STREAM_NAME', 'ride_predictions')
shard_id = 'shardId-000000000000'

# Get the Shard Iterator with TRIM_HORIZON to read from the beginning of the stream
shard_iterator_response = kinesis_client.get_shard_iterator(
    StreamName = stream_name,
    ShardId = shard_id,
    ShardIteratorType = 'TRIM_HORIZON',
)

shard_iterator_id = shard_iterator_response['ShardIterator']

# Read records from the stream
records_response = kinesis_client.get_records(
    ShardIterator = shard_iterator_id,
    Limit = 1
)

records = records_response['Records']
pprint(records)

assert len(records) == 1


# Read the actual response from the record
actual_record = json.loads(records[0]['Data'])
pprint(actual_record)

# Extract the prediction from the record
expected_records = {
    'model': 'ride_duration_prediction_model',
    'version': '3ec150b70a5549769f4acd9bc09da04b',
    'prediction': {
        'ride_duration': 18.18,
        'ride_id': 256
    }
}

# Test for the different fields in the response
diff = DeepDiff(actual_record, expected_records, significant_digits=2)
print(f'diff: {diff}')

assert 'type_changes' not in diff
assert 'value_changes' not in diff

print('Test passed! The actual record matches the expected record.')