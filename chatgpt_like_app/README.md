

# Architecture

```text
+------------------------------------------------------+
|                    Windows Laptop                    |
|                                                      |
|   Browser                                            |
|      |                                               |
|      | http://localhost:8080                         |
|      ▼                                               |
| +-----------------------------------------------+    |
| |            Ubuntu WSL                         |    |
| |                                               |    |
| |  +----------------+      +----------------+   |    |
| |  | Open WebUI     | ---> | Ollama Server  |   |    |
| |  | Docker         |      | localhost:11434|   |    |
| |  +----------------+      +----------------+   |    |
| |                                |              |    |
| |                          llama3.2:1b          |    |
| +-----------------------------------------------+    |
+------------------------------------------------------+
```

---

# Step 1: Install Ollama

Install Ollama inside Ubuntu WSL.

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify installation.

```bash
ollama --version
```

---

# Step 2: Start Ollama

Initially start Ollama.

```bash
ollama serve
```

or if installed as a service

```bash
sudo systemctl start ollama
```

Check status.

```bash
systemctl status ollama
```

---

# Step 3: Download the Llama model

Download Llama 3.2 1B.

```bash
ollama pull llama3.2:1b
```

Verify.

```bash
ollama list
```

Output

```text
NAME
llama3.2:1b
```

---

# Step 4: Install Docker Engine inside WSL

Install Docker Engine (Community Edition).

Verify installation.

```bash
docker version
```

You should see

```text
Client: Docker Engine
Server: Docker Engine
```

---

# Step 5: Pull Open WebUI image

```bash
docker pull ghcr.io/open-webui/open-webui:main
```

---

# Step 6: Start Open WebUI (initial attempt)

Initially we started it using

```bash
docker run -d \
  --name open-webui \
  -p 3000:3080 \
  ghcr.io/open-webui/open-webui:main
```

Problem:

```
localhost:3000
```

did not open.

Reason:

The container actually listens on

```
8080
```

not

```
3080
```

---

# Step 7: Correct Docker port mapping

Correct command:

```bash
docker rm -f open-webui

docker run -d \
  --name open-webui \
  -p 3000:8080 \
  ghcr.io/open-webui/open-webui:main
```

---

# Step 8: Verify Open WebUI

Inside the container:

```bash
docker exec -it open-webui bash
```

Check listening port.

```bash
ss -tulnp
```

Output

```
0.0.0.0:8080
```

---

# Step 9: Problem - No models in Open WebUI

Browser showed

```
No models available
```

or

```
Failed to fetch models
```

Error:

```
Cannot connect to host
host.docker.internal:11434
```

---

# Step 10: Verify Ollama

Check models.

```bash
ollama list
```

Output

```
llama3.2:1b
```

Check API.

```bash
curl http://localhost:11434/api/tags
```

Expected JSON

```json
{
  "models":[
      {
          "name":"llama3.2:1b"
      }
  ]
}
```

---

# Step 11: Find the root cause

Initially

```bash
ss -tulnp | grep 11434
```

showed

```
127.0.0.1:11434
```

Meaning

Ollama was only accepting localhost connections.

Docker container couldn't access it.

---

# Step 12: Configure Ollama to listen on all interfaces

Since Ollama was running as a **systemd service**, we created an override.

```bash
sudo systemctl edit ollama
```

Added

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Reload.

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

Verify.

```bash
ss -tulnp | grep 11434
```

Output

```
*:11434
```

Now Ollama accepts external connections.

---

# Step 13: Start Open WebUI using Host Network

Since Docker Engine is running inside WSL, we used host networking.

```bash
docker rm -f open-webui

docker run -d \
  --name open-webui \
  --network host \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  -v open-webui:/app/backend/data \
  --restart unless-stopped \
  ghcr.io/open-webui/open-webui:main
```

Notice

There is **no `-p` option** because host networking shares the host network namespace.

Open WebUI is then available on:

```
http://localhost:8080
```

---

# Step 14: Verify connectivity from inside the container

Run

```bash
docker exec -it open-webui curl http://127.0.0.1:11434/api/tags
```

Output

```json
{
  "models":[
      {
          "name":"llama3.2:1b"
      }
  ]
}
```

This proved:

* Docker → Ollama connectivity ✅
* Ollama API working ✅
* Model detected ✅

---

# Step 15: Final Open WebUI configuration

The remaining issue was inside Open WebUI.

Initially it was configured to use

```
http://host.docker.internal:11434
```

This was incorrect for your WSL setup.

Go to:

```
Open WebUI
   ↓
Settings
   ↓
Connections
   ↓
Ollama
```

Change

```
http://host.docker.internal:11434
```

to

```
http://127.0.0.1:11434
```

Save the configuration.

---

# Step 16: Verify models

After saving the connection,

Go to

```
Settings
   ↓
Models
```

or

```
Select Model
```

You should now see

```
llama3.2:1b
```

---

# Final Working Configuration

### Ollama

```
Running inside Ubuntu WSL
```

Listening on

```
*:11434
```

---

### Open WebUI

Running inside Docker.

```
--network host
```

Environment variable

```
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

---

### Browser

Open

```
http://localhost:8080
```

---

# Useful Commands

### List models

```bash
ollama list
```

### Run a model

```bash
ollama run llama3.2:1b
```

### Check Ollama API

```bash
curl http://127.0.0.1:11434/api/tags
```

### View Open WebUI logs

```bash
docker logs -f open-webui
```

### Restart Open WebUI

```bash
docker restart open-webui
```

### Restart Ollama

```bash
sudo systemctl restart ollama
```

### Check listening ports

```bash
ss -tulnp
```

---


* Open WebUI listens on **port 8080**, not 3080.
* Ollama running only on `127.0.0.1` cannot be reached by Docker containers using bridge networking.
* In a native WSL Docker Engine setup, `--network host` simplifies communication between Docker and Ollama.
* When using host networking, `-p` port mapping is ignored.
* Open WebUI's **Connections** setting must point to the correct Ollama endpoint. In your setup, `http://127.0.0.1:11434` was the correct URL.
* Always verify connectivity using the Ollama API (`/api/tags`) before troubleshooting the Open WebUI interface.

With this configuration, your local AI stack is fully operational: **Browser → Open WebUI (Docker) → Ollama (WSL) → `llama3.2:1b`**.
