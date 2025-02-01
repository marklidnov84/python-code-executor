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

Response:
```json
{
    "result": {
        "last": "lidnov",
        "name": "mark"
    },
    "stdout": ""
}
