ROLE: You are an SRE writing a blameless post-incident review.
 
CONTEXT: CloudCart e-commerce SaaS. Audience is the engineering team plus one
executive summary paragraph for non-technical leadership.
 
DATA:
INCIDENT: CloudCart Inventory Service Outage
DATE: 2026-07-21   DURATION: 12 minutes   SEVERITY: SEV-2
 
TIMELINE:
14:03:00  Pipeline triggered by merge to main (PR #847)
14:03:45  Image built and pushed as inventory:a1b2c3d  (7-character SHA)
14:04:02  Deploy step ran: kubectl set image ... inventory:a1b2c3d7  (8 characters)
14:04:20  New pod entered ImagePullBackOff: manifest not found
14:05:00  Orders service log: connection refused to inventory:3002
14:05:30  Alert fired: inventory-pod-not-ready exceeded 60s
14:06:00  On-call engineer acknowledged
14:09:00  Root cause identified
14:10:00  Rollback issued: kubectl rollout undo deployment/inventory
14:11:30  Previous revision passed readiness probe
14:12:00  Orders service reconnected; 502 errors stopped
 
IMPACT:
- Inventory API unavailable 7 minutes 45 seconds
- 23 orders failed at the stock-check step
- 847 frontend requests returned HTTP 502
- No data loss; inventory database unaffected
 
SYSTEM CONTEXT:
- Build step uses: git rev-parse --short=7 HEAD
- Deploy script uses: git rev-parse --short=8 HEAD
- No image-existence check before kubectl set image
- No automated rollback on deploy failure
- Deployment progressDeadlineSeconds is 600 (10 minutes)
    
TASK: Produce a root cause analysis document.
 
CONSTRAINTS:
- Every claim must reference an item from the DATA section.
- Use 5-Why analysis to reach the root cause.
- Blameless: no individual named or implied at fault.
- Executive summary must be 80 words or fewer.
 
FORMAT: Executive Summary / Timeline / 5-Why Root Cause /
Contributing Factors / Action Items"
