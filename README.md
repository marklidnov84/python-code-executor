### Python Remote Executor API Service

This service allows customers to execute arbitrary Python code on a cloud server. By sending a Python script to an API endpoint, the execution result of the main() function is returned as a JSON object.

The service is built using Flask and nsjail, ensuring a safe execution environment for the Python scripts.
