import subprocess
from .base_workspace import *


class E2BWorkspace(Workspace):
    def __init__(self, workspace_id: str):
        self.sandbox_id = workspace_id
        self.sandbox = None  # Assuming a sandbox object needs to be managed

    def setup(self, env: WorkspaceEnv, **kwargs):
        # Setup the E2B sandbox environment
        pass

    def reset(self):
        # Reset the sandbox to its initial state
        pass

    def communicate(self, cmd: Command, timeout: int) -> BaseCmdResponse:
        if self.sandbox is None:
            raise ValueError("Sandbox is None")
        result = subprocess.run(
            ["e2b-sandbox-cli", "exec", self.sandbox_id, cmd.get_cmd_str()],
            capture_output=True,
            text=True
        )
        return BaseCmdResponse(output=result.stdout, retunr_code=result.returncode)

    def get_state(self) -> dict:
        state_result = subprocess.run(
            ["e2b-sandbox-cli", "state", self.sandbox_id],
            capture_output=True,
            text=True
        )
        return {"sandbox_id": self.sandbox_id, "state": state_result.stdout}

    def close(self):
        # Close the sandbox
        pass