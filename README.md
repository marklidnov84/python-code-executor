### Python Remote Executor API Service

This service allows customers to execute arbitrary Python code on a cloud server. By sending a Python script to an API endpoint, the execution result of the main() function is returned as a JSON object.

The service is built using Flask and nsjail, ensuring a safe execution environment for the Python scripts.

### Business Context

The goal of this service is to enable customers to execute Python scripts remotely on a cloud server. The user sends a Python script to the /execute endpoint, and the service executes the script in a secure environment, returning the result of the script’s main() function.

The service ensures the security of script execution by using nsjail in a Docker container.

### API Documentation

#### Request Example

To send a request to the API, use the following cURL command:

```curl
curl --location 'https://python-code-executor-239153248383.us-west1.run.app/execute' \
--header 'Content-Type: application/json' \
--data '{
    "script": "def main():\n first_name = \"mark\" \n last_name = \"lidnov\" \n return {\"name\": first_name, \"last\": last_name}"
}'
```
AND

```curl
curl --location 'https://python-code-executor-239153248383.us-west1.run.app/execute' \
--header 'Content-Type: application/json' \
--data '{"script": "class MyCustomClass:\n    def __init__(self, name, value):\n        self.name = name\n        self.value = value\n\ndef main():\n    return MyCustomClass(\"example\", 42)"}'
```

### Deploy With Docker

To run the service locally with Docker run this command:

```
docker build -t python-remote-executor . && docker run --rm -p 8080:8080 python-remote-executor
```

Hence you'll be able to call locally like this:

````curl
```curl
curl --location 'http://localhost:8080/execute' \
--header 'Content-Type: application/json' \
--data '{
    "script": "def main():\n first_name = \"mark\" \n last_name = \"lidnov\" \n return {\"name\": first_name, \"last\": last_name}"
}'
````

### Deploying on Google Cloud

1. Deploy to Google Cloud Run container service

```
gcloud run deploy --allow-unauthenticated --allow-unencrypted-build --breakglass="running nsjail" --execution-environment=gen2 --source .
```
