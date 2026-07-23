## Prompt
Write a complete bash script named ns-janitor.sh.
 
Behaviour:
- Takes a namespace as the first argument.
- Accepts a --delete flag in any position. Without it, the script is dry-run only.
- Finds pods in Failed, Succeeded, or Evicted state that are older than the
  AGE_THRESHOLD_SECONDS environment variable (default 3600).
- Prints a table: POD | STATUS | AGE | CREATED_AT
- Deletes matching pods only when --delete is supplied.
 
Requirements:
- Start with set -euo pipefail.
- Print a usage message and exit 1 if no namespace is given.
- Exit 1 with a clear error if the namespace does not exist.
- Exit 0 with a message if there is nothing to clean.
- Log every action with an ISO 8601 timestamp to ./ns-janitor.log.
- Use only bash and kubectl. Do not use jq.
- Add a comment explaining the age calculation logic.
 
Output the script only, with no surrounding explanation."
