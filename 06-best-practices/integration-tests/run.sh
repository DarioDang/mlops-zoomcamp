#!/usr/bin/env bash



cd "$(dirname "$0")" # This make sure always navigate to the script directory

LOCAL_TAG=$(date +%Y-%m-%d_%H-%M)
export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"
export PREDICTIONS_STREAM_NAME="ride_predictions"

docker build -t ${LOCAL_IMAGE_NAME} ../code

docker-compose up -d  

# Wait for LocalStack to be ready
echo "Waiting for Kinesis to be ready..."
until aws --endpoint-url=http://localhost:4566 kinesis list-streams >/dev/null 2>&1; do
  sleep 2
done
echo "Kinesis is ready."

aws --endpoint-url=http://localhost:4566 \
    --region ap-southeast-2 \
    kinesis create-stream \
    --stream-name ${PREDICTIONS_STREAM_NAME} \
    --shard-count 1

pipenv run python test-docker.py 

ERROR_CODE=$?

if [ $ERROR_CODE != 0 ]; then
    echo "Integration tests failed with error code: $ERROR_CODE"
    docker-compose down
    exit $ERROR_CODE
fi

# If it not fail, run the kinesis test
pipenv run python test-kinesis.py 

ERROR_CODE=$?

if [ $ERROR_CODE != 0 ]; then
    echo "Integration tests failed with error code: $ERROR_CODE"
    docker-compose down
    exit $ERROR_CODE
fi

docker-compose down


