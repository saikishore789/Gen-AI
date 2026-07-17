"""Prompt templates for the LLM diagnosis."""

from textwrap import dedent


DIAGNOSIS_PROMPT = dedent(
    """
    You are a senior Kubernetes site reliability engineer.

    Investigate the following {scenario} issue using only the read-only cluster state
    provided. Return a concise Markdown diagnosis that includes:

    1. A short summary of what is happening.
    2. Likely root causes.
    3. Suggested next commands or remediation steps.

    Cluster state:
    {cluster_state}
    """
).strip()


def build_diagnosis_prompt(scenario: str, cluster_data: dict[str, dict[str, str]]) -> str:
    """Build a diagnosis prompt from scenario and kubectl output."""
    state_parts = []
    for command, result in cluster_data.items():
        state_parts.append(f"### kubectl {command}")
        if result["stdout"]:
            state_parts.append("```")
            state_parts.append(result["stdout"])
            state_parts.append("```")
        if result["stderr"]:
            state_parts.append("**stderr:**")
            state_parts.append("```")
            state_parts.append(result["stderr"])
            state_parts.append("```")
        state_parts.append(f"**exit code:** {result['returncode']}")

    cluster_state = "\n".join(state_parts)
    return DIAGNOSIS_PROMPT.format(scenario=scenario, cluster_state=cluster_state)
