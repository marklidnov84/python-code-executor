from flask import Flask, request, jsonify
import subprocess
import json
import tempfile
import os

# file name
app = Flask(__name__)

def validate_script(script):
    # Validate that the script contains a main() function and returns JSON.
    if "def main():" not in script:
        return False, "Script must contain a main() function"
    return True, None

def execute_script_safely(script: str):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        # wrap the script to ensure it returns JSON
        wrapped_script = f"""
import sys
import json
import pandas as pd
import numpy as np
import os

{script}

if __name__ == "__main__":
    try:
        result = main()
        # Validate that result is JSON serializable
        json_result = json.dumps(result)
        print("---RESULT_SEPARATOR---")
        print(json_result)
    except Exception as e:
        print(f"Error during execution: {{str(e)}}", file=sys.stderr)
        sys.exit(1)
"""
        f.write(wrapped_script)
        script_path = f.name

    try:
        # run the script inside NSJail
        cmd = [
            "nsjail",
            "--config", "/app/nsjail.cfg",
            "--",
            "/usr/bin/python3", script_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

        stderr_output = result.stderr.strip()
        stdout_parts = result.stdout.split("---RESULT_SEPARATOR---")

        if result.returncode != 0:
            return None, stderr_output or "Execution failed", 400

        if len(stdout_parts) != 2:
            return None, "Script did not return valid JSON", 400
        
        try:
            # attempt to deserialize the JSON result
            result = json.loads(stdout_parts[1].strip())
            return result, stdout_parts[0].strip(), None
        except TypeError:
            return None, "Script did not return valid JSON", 400
    
    except subprocess.TimeoutExpired:
        return None, "Script execution timed out", 400
    finally:
        os.unlink(script_path)
    
@app.route('/execute', methods=["POST"])
def execute():
    # handle POST requests to execute Python scripts

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    if 'script' not in data:
        return jsonify({"error": "Request must contain 'script' field"}), 400

    script = data['script']
    if not isinstance(script, str):
        return jsonify({"error": "Script must be a string"}), 400

    # validate script
    is_valid, error = validate_script(script)
    if not is_valid:
        return jsonify({"error": error}), 400

    # execute script
    result, stdout, error = execute_script_safely(script)
    if error:
        return jsonify({"stdout": stdout, "error": error}), 400

    return jsonify({
        "result": result,
        "stdout": stdout
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
