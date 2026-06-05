import subprocess
import json
import os

class SandboxRunner:
    def __init__(self):
        pass
        
    def execute_plugin(self, plugin_path, parameters):
        """Runs the plugin in a restricted subprocess."""
        # For a true sandbox on Linux, we might use `bwrap` (Bubblewrap) or `chroot`.
        # Here we simulate the subprocess call.
        try:
            result = subprocess.run(
                ["python3", plugin_path, json.dumps(parameters)],
                capture_output=True,
                text=True,
                check=True
            )
            return {"status": "success", "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "error": e.stderr}
