"""Scenario-specific command maps and data gatherers."""

from k8s_troubleshooting_agent.kubectl import KubectlRunner


SCENARIO_COMMANDS: dict[str, list[list[str]]] = {
    "pod": [
        ["get", "pods", "-o", "wide"],
        ["events", "--field-selector", "involvedObject.kind=Pod"],
    ],
    "resource": [
        ["get", "deployments"],
        ["get", "replicasets"],
        ["get", "daemonsets"],
        ["get", "statefulsets"],
        ["get", "events"],
    ],
    "networking": [
        ["get", "services"],
        ["get", "ingresses"],
        ["get", "networkpolicies"],
    ],
    "storage": [
        ["get", "persistentvolumeclaims"],
        ["get", "persistentvolumes"],
        ["get", "storageclasses"],
    ],
    "node": [
        ["get", "nodes", "-o", "wide"],
        ["top", "nodes"],
    ],
}


def gather_scenario_data(
    kubectl: KubectlRunner,
    scenario: str,
    name: str | None = None,
) -> dict[str, dict[str, str]]:
    """Gather read-only kubectl output for the requested scenario."""
    if scenario not in SCENARIO_COMMANDS:
        raise ValueError(f"unknown scenario: {scenario}")

    results: dict[str, dict[str, str]] = {}
    for command in SCENARIO_COMMANDS[scenario]:
        full_command = list(command)
        if name is not None:
            full_command.append(name)
        key = " ".join(full_command)
        result = kubectl.run(*full_command)
        results[key] = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": str(result.returncode),
        }
    return results
