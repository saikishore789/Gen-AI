"""Command-line interface for the Kubernetes troubleshooting agent."""

import argparse
import sys

from k8s_troubleshooting_agent import __version__
from k8s_troubleshooting_agent.agent import run_diagnosis


SCENARIOS = ["pod", "resource", "networking", "storage", "node"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="k8s-troubleshooting-agent",
        description="Diagnose Kubernetes issues using an LLM.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--provider",
        required=True,
        help="LLM provider to use (e.g., openai, ollama, anthropic).",
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Model name to use with the selected provider.",
    )
    parser.add_argument(
        "--namespace",
        default="default",
        help="Kubernetes namespace to scope the investigation.",
    )
    parser.add_argument(
        "--kubeconfig",
        default=None,
        help="Path to a kubeconfig file.",
    )
    subparsers = parser.add_subparsers(dest="scenario", help="Troubleshooting scenario")
    for scenario in SCENARIOS:
        sub = subparsers.add_parser(scenario, help=f"Diagnose {scenario} issues")
        sub.add_argument("--name", default=None, help="Resource name to focus on")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.scenario is None:
        parser.error("choose a scenario: " + ", ".join(SCENARIOS))

    result = run_diagnosis(args)
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
