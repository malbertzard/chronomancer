from dataclasses import dataclass, field
from typing import List, Literal, Optional
import subprocess

ConnectionType = Literal["local", "ssh"]

@dataclass
class Host:
    name: str
    connection: ConnectionType = "local"
    user: Optional[str] = None
    hostname: Optional[str] = None
    ssh_options: Optional[List[str]] = field(default_factory=list)

    def _build_ssh_command(self, remote_cmd: str) -> List[str]:
        if not self.user or not self.hostname:
            raise ValueError("SSH requires both user and hostname")

        cmd = ["ssh"]
        if self.ssh_options:
            cmd.extend(self.ssh_options)

        cmd.append(f"{self.user}@{self.hostname}")
        cmd.append(remote_cmd)
        return cmd

    def run(self, command: str) -> str:
        if self.connection == "local":
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        elif self.connection == "ssh":
            cmd = self._build_ssh_command(command)
            result = subprocess.run(cmd, capture_output=True, text=True)
        else:
            raise ValueError(f"Unsupported connection type: {self.connection}")

        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {result.stderr.strip()}")

        return result.stdout.strip()

    def read_crontab(self, user: Optional[str] = None) -> str:
        cmd = f"crontab -l"
        if user:
            cmd += f" -u {user}"
        return self.run(cmd)

    def read_file(self, path: str) -> str:
        if self.connection == "local":
            with open(path, "r") as f:
                return f.read()
        else:
            return self.run(f"cat {path}")
