ROLE: You are a cloud security engineer reviewing Terraform for Azure.
 
CONTEXT: CloudCart is a regulated e-commerce SaaS. Our standards:
- No public IPs on internal services
- All storage encrypted at rest, TLS 1.2 minimum
- RBAC with least privilege; no admin accounts on registries
- Mandatory tags on every resource: env, owner, cost-center
 
DATA:
resource "azurerm_storage_account" "orders_data" {
  name                     = "cloudcartorders"
  resource_group_name      = "cloudcart-rg"
  location                 = "eastus"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
 
resource "azurerm_kubernetes_cluster" "cloudcart" {
  name                = "cloudcart-aks"
  location            = "eastus"
  resource_group_name = "cloudcart-rg"
  dns_prefix          = "cloudcart"
  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_DS2_v2"
  }
  identity { type = "SystemAssigned" }
}
 
resource "azurerm_public_ip" "orders_api" {
  name                = "orders-public-ip"
  resource_group_name = "cloudcart-rg"
  location            = "eastus"
  allocation_method   = "Static"
}
 
resource "azurerm_container_registry" "acr" {
  name                = "cloudcartacr"
  resource_group_name = "cloudcart-rg"
  location            = "eastus"
  sku                 = "Basic"
  admin_enabled       = true
}
 
resource "azurerm_redis_cache" "cache" {
  name                = "cloudcart-redis"
  location            = "eastus"
  resource_group_name = "cloudcart-rg"
  capacity            = 1
  family              = "C"
  sku_name            = "Basic"
  enable_non_ssl_port = true
}


 
TASK: Review this Terraform against the standards above.
 
CONSTRAINTS:
- Cite the exact resource block for every finding.
- Severity scale: CRITICAL / HIGH / LOW.
- Identify issues only. Do not rewrite the code.
 
FORMAT: A table with columns: Resource | Finding | Severity | Fix
