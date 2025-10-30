import subprocess
import json
from pathlib import Path

CONFIG_PATH = Path("openspec/.github-config.json")

class GitHubIntegration:
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        return {"enabled": False}

    def run(self, *args):
        return subprocess.run(args, capture_output=True, text=True, check=False)

    def enabled(self):
        return self.config.get("enabled", False)

    def commit(self, message: str):
        if not self.enabled():
            return
        self.run("git", "add", ".")
        self.run("git", "commit", "-m", message)
        self.run("git", "push", "origin", "main")

    def status(self):
        return self.run("git", "status").stdout

    def sync(self):
        if not self.enabled():
            return "Integration disabled"
        self.run("git", "pull", "--rebase", "origin", "main")
        self.run("git", "push", "origin", "main")
        return "Sync complete"

if __name__ == "__main__":
    gh = GitHubIntegration()
    print(gh.status())
