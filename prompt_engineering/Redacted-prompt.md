## Token budget
- Extract, do not dump. Use get + events, not describe.
- Prompts over ~1000 tokens need a one-line justification.
 
## Redaction — run before every paste
(Get-Content <file>) |
ForEach-Object {
    $_ `
    -replace '(PASSWORD|KEY|SECRET|TOKEN|CREDENTIAL|CONNECTION_STRING)=.*', '$1=<REDACTED>' `
    -replace '(://[^:@/]*:)[^@]+(@)', '$1<REDACTED>$2' `
    -replace '(AccountKey=)[^;]+(;)', '$1<REDACTED>$2'
}

## Data

ORDERS_DB_HOST=orders-db.cloudcart.internal
ORDERS_DB_PASSWORD=Pr0duction!2026
INVENTORY_API_KEY=inv_live_8xKm9pQ2rT5Yz
STRIPE_SECRET_KEY=sk_live_51HxT9zKfakeValue999
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=store;AccountKey=fAkEkEy123==;
REDIS_URL=redis://:cloudcart-redis-secret-2026@redis.cache.windows.net:6380/0
ACR_ADMIN_PASSWORD=acr-pass-456
AZURE_CLIENT_SECRET=8Qz~FAKEclientSecret
JWT_SIGNING_KEY=jwt-hmac-secret-

Then read the output yourself. Regexes miss inline credentials,
base64 blobs, and anything in an unexpected format.
 
## Never paste
- .env files, kubeconfig, service account JSON, TLS private keys
- Anything retrieved from a secrets manager
