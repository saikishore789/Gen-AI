"""Safe, read-only kubectl runner."""

import shlex
import subprocess
from dataclasses import dataclass
from typing import Any


READONLY_COMMANDS = {
    "get",
    "describe",
    "logs",
    "top",
    "events",
    "version",
    "api-resources",
    "api-versions",
}


@dataclass
class KubectlResult:
    stdout: str
    stderr: str
    returncode: int


@dataclass
class KubectlRunner:
    kubeconfig: str | None = None
    namespace: str = "default"
    context: str | None = None

    def run(self, *args: str, **kwargs: Any) -> KubectlResult:
        """Run a kubectl command, rejecting non-read-only verbs."""
        if not args:
            raise ValueError("kubectl command must contain at least one argument")
        if args[0] not in READONLY_COMMANDS:
            raise ValueError(f"refusing to run non-read-only kubectl verb: {args[0]}")

        cmd = ["kubectl"]
        if self.kubeconfig:
            cmd.extend(["--kubeconfig", self.kubeconfig])
        if self.context:
            cmd.extend(["--context", self.context])
        cmd.extend(["--namespace", self.namespace])
        cmd.extend(args)

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                **kwargs,
            )
        except FileNotFoundError as exc:
            raise RuntimeError("kubectl binary not found on PATH") from exc

        return KubectlResult(
            stdout=proc.stdout,
            stderr=proc.stderr,
            returncode=proc.returncode,
        )

    def safe_command(self, command: str) -> KubectlResult:
        """Parse and run a safe kubectl command string."""
        parts = shlex.split(command)
        return self.run(*parts)
