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
curl --location 'http://34.168.137.155:8080/execute' \
--header 'Content-Type: application/json' \
--data '{
    "script": "def main():\n first_name = \"mark\" \n last_name = \"lidnov\" \n return {\"name\": first_name, \"last\": last_name}"
}'
```

Response:
```json
{
    "result": {
        "last": "lidnov",
        "name": "mark"
    },
    "stdout": ""
}
```

### Deploy With Docker

To run the service locally with Docker run this command:
```
docker build -t python-remote-executor . && docker run --rm -p 8080:8080 python-remote-executor
```

Hence you'll be able to call locally like this:

```curl
```curl
curl --location 'http://localhost:8080/execute' \
--header 'Content-Type: application/json' \
--data '{
    "script": "def main():\n first_name = \"mark\" \n last_name = \"lidnov\" \n return {\"name\": first_name, \"last\": last_name}"
}'
```

### Deploying on Google Cloud

1. Push the docker image to GCR
```
docker tag python-remote-executor gcr.io/YOUR_PROJECT_ID/python-remote-executor && docker push gcr.io/YOUR_PROJECT_ID/python-remote-executor
```

2. Deploy Docker image on Google Cloud
```
gcloud compute instances create-with-container nsjail-vm \
    --container-image=gcr.io/YOUR_PROJECT_ID/python-remote-executor \
    --container-privileged \
    --tags=python-executor \
    --container-env=FLASK_ENV=production \
    --scopes=cloud-platform
```

3. Expose the VM to the internet:
```
gcloud compute firewall-rules create python-allow-http \
    --allow=tcp:8080 \
    --target-tags=python-executor
```
4. The service will now be accessible at the external IP of your VM.
