LOCAL_TAG=$(shell date +"%Y-%m-%d_%H-%M")
LOCAL_IMAGE_NAME:=stream-model-duration:${LOCAL_TAG}

test:
	pytest tests/

quality_checks:
	isort . 
	black .
	pylint --recursive=y .

build: quality_checks test  
	docker build -t ${LOCAL_IMAGE_NAME} ./code

integration_test: build
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash integration-tests/run.sh 

publish: build integration_test
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash scripts/publish.sh
