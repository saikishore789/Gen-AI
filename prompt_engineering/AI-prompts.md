## CI/CD File creation
## Jenkins file
==============================
Generate a complete Jenkinsfile for CloudCart.
 
CONTEXT: Go 1.22 microservices, multi-stage Docker builds. Registry is Azure
Container Registry cloudcartcr . Deploy target is AKS, namespace cloudcart.
 
Stages: lint (golangci-lint) > test (go test -race) > build image >
scan (Trivy) > push to ACR > deploy staging > manual approval > deploy production.
 
Requirements: pin all tool versions; use the Jenkins credentials store for every
secret; include a rollback stage triggered on deploy failure; tag images with the
git SHA; comment non-obvious steps.
 
Output the Jenkinsfile only.
==============================

## Gitlab CI file
==============================
Generate a complete .gitlab-ci.yml for CloudCart.
 
CONTEXT: Go 1.22 microservices, multi-stage Docker builds. Registry is Azure
Container Registry cloudcartcr. Deploy target is AKS, namespace cloudcart.
 
Stages: lint (golangci-lint) > test (go test -race) > build image >
scan (Trivy) > push to ACR > deploy staging > manual approval > deploy production.
 
Requirements: pin all image versions; use GitLab CI/CD variables for every secret;
include a rollback job triggered on deploy failure; tag images with the git SHA;
comment non-obvious steps.
 
Output the YAML only.
==============================


## AI prompt
=============================
ROLE: You are a cloud security engineer reviewing Terraform for Azure.
 
CONTEXT: CloudCart is a regulated e-commerce SaaS. Standards: TLS 1.2 minimum on all
storage; no public blob access; no management ports open to the internet; RBAC and
Azure AD required on AKS clusters; production workloads must not live in a staging
resource group; every resource must carry env and owner tags.
 
DATA:
use the content from flawed/flawed.tf
 
TASK: Review this Terraform against the standards above.
 
CONSTRAINTS: Cite the exact resource block for every finding. Severity CRITICAL /
HIGH / LOW. Identify issues only, do not rewrite the code.
 
FORMAT: Table with columns Resource | Finding | Severity | Fix
=============================


Create a compliance.rego file using the below prompt
=======================
You are a policy-as-code engineer.
 
Convert these compliance requirements into OPA Rego policies that run against
Terraform plan JSON via conftest:
 
All storage must be encrypted in transit with TLS 1.2 minimum, no storage may allow
public blob access, and every resource must carry env and owner tags.
 
Requirements:
- package main
- One deny rule per requirement, three in total
- Each deny message must name the offending resource address
- Iterate over input.resource_changes and inspect .change.after
- Use conftest-compatible syntax
- Guard against null values so the policy does not error on resources that lack
  the attribute
 
Output only a single fenced code block containing the .rego file." create the file uder policy folder
============================

## Cost analysis and anamoly detection
================================
Prompt:
ROLE: You are a FinOps analyst reviewing CloudCart’s monthly Azure cost export.
The bill grew sharply in one quarter and nobody knows why.
 
TASK: Analyse this export and produce:
1. Total monthly spend, and a breakdown by resource group.
2. The top 5 cost anomalies, with evidence quoted from the data. An anomaly
   is spend that looks wasteful, orphaned, oversized for its utilisation,
   or unexplained.
3. For each anomaly: estimated monthly saving and the exact Azure remediation
   (CLI command or SKU change).
4. Anything you would flag for investigation BEFORE taking action.

DATA:
Consider the finops data for this analysis

CONSTRAINTS:
- Reference specific resource names from the data.
- Do not recommend action on resources whose utilisation suggests they are
  legitimately busy.
- State your arithmetic so it can be checked.
============================
