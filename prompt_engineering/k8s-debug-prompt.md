ROLE: You are a senior Kubernetes SRE.

CONTEXT: AKS v1.29, 3 nodes, namespace "cloudcart" running three Go
microservices (frontend, orders, inventory). Recent change:
=== Recent Events ===
Type     Reason     Age                   From               Message
  ----     ------     ----                  ----               -------
  Normal   Scheduled  23m                   default-scheduler  Successfully assigned cloudcart/inventory-759759bccf-f658q to aks-agentpool-31893281-vmss000004
  Normal   Pulling    21m (x5 over 23m)     kubelet            spec.containers{inventory}: Pulling image "hashicorp/http-echo:does-not-exist-v99"
  Warning  Failed     21m (x5 over 23m)     kubelet            spec.containers{inventory}: Failed to pull image "hashicorp/http-echo:does-not-exist-v99": rpc error: code = NotFound desc = failed to pull and unpack image "docker.io/hashicorp/http-echo:does-not-exist-v99": failed to resolve image: docker.io/hashicorp/http-echo:does-not-exist-v99: not found
  Warning  Failed     21m (x5 over 23m)     kubelet            spec.containers{inventory}: Error: ErrImagePull
  Normal   BackOff    3m58s (x86 over 23m)  kubelet            spec.containers{inventory}: Back-off pulling image "hashicorp/http-echo:does-not-exist-v99"
  Warning  Failed     3m58s (x86 over 23m)  kubelet            spec.containers{inventory}: Error: ImagePullBackOff

DATA:
=== Pod Status ===
NAME                          READY   STATUS             RESTARTS   AGE
broken-app-8544498f4d-c5mjx   1/1     Running            0          21h
frontend-766f79bc76-pzz2f     1/1     Running            0          21h
frontend-766f79bc76-xm5wn     1/1     Running            0          21h
inventory-5c69558b8-pjxg4     1/1     Running            0          21h
inventory-759759bccf-f658q    0/1     ImagePullBackOff   0          24m
orders-66d8b6bfc7-dfsdk       1/1     Running            0          21h
orders-66d8b6bfc7-smn24       1/1     Running            0          21h

TASK: Diagnose the issue shown in the data.

CONSTRAINTS:
- Base findings ONLY on the data provided. If the data is insufficient,
  say what else you need. Do not speculate.
- Suggest only non-destructive commands.
- Flag any suggestion that would cause downtime with [DOWNTIME].

FORMAT:
1) Finding
2) Evidence (quote the exact line from DATA)
3) Next command to run
