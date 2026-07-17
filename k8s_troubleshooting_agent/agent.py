"""Orchestrator that gathers cluster state and calls the LLM for a diagnosis."""

from dataclasses import dataclass

from k8s_troubleshooting_agent.kubectl import KubectlRunner
from k8s_troubleshooting_agent.llm import create_llm
from k8s_troubleshooting_agent.prompts import build_diagnosis_prompt
from k8s_troubleshooting_agent.scenarios import gather_scenario_data


@dataclass
class DiagnosisArgs:
    provider: str
    model: str
    namespace: str
    kubeconfig: str | None
    scenario: str
    name: str | None


def run_diagnosis(args: DiagnosisArgs) -> str:
    """Run a read-only diagnosis for the requested scenario."""
    kubectl = KubectlRunner(kubeconfig=args.kubeconfig, namespace=args.namespace)
    cluster_data = gather_scenario_data(kubectl, args.scenario, args.name)
    llm = create_llm(args.provider, args.model)
    prompt = build_diagnosis_prompt(args.scenario, cluster_data)
    return llm.predict(prompt)
