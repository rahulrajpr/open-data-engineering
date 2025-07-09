# Airbyte Production Installation Guide (abctl-based)

## ❓ Why Not Docker Compose?

As of **June 2024**, Airbyte officially deprecated Docker Compose for production use. Here's why:

* ⚠️ **Incompatible after v1.0** (expected August 2024)
* 🧱 No support for scaling (multiple workers, load balancing)
* ❌ Manual state recovery (fragile volume management)
* 🚫 Poor upgrade support

➡️ Instead, use `abctl` — a CLI tool to install Airbyte on Kubernetes using `kind` and Helm — aligning with production-grade setups.

---

## ✅ Prerequisites

* Ubuntu system (VM or bare metal)
* Docker Engine installed (`docker run hello-world` should work)
* 4+ CPUs, 8+ GB RAM recommended (use `--low-resource-mode` if less)
* Internet access

---

## 🔧 Step 1: Install `abctl`

```bash
mkdir -p ~/abctl-install && cd ~/abctl-install
curl -LO https://github.com/airbytehq/abctl/releases/download/v0.28.0/abctl-v0.28.0-linux-amd64.tar.gz
tar -xvzf abctl-v0.28.0-linux-amd64.tar.gz
sudo mv abctl-v0.28.0-linux-amd64/abctl /usr/local/bin/
sudo chmod +x /usr/local/bin/abctl
abctl version
```

---

## 🐘 Step 2: Run PostgreSQL in Docker

Airbyte requires persistent storage for metadata. We will run a Dockerized PostgreSQL instance:

```bash
docker run -d \
  --name airbyte-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin123 \
  -e POSTGRES_DB=opende \
  -p 5434:5432 \
  postgres
```

Confirm connection:

```bash
psql -h localhost -p 5434 -U admin -d opende
```

Password: `admin123`

---

## 📝 Step 3: Create values.yaml

Create this file:

```bash
nano ~/openDE/open-data-engineering/airbyte-values.yaml
```

Paste the following:

```yaml
global:
  edition: community

database:
  host: host.docker.internal
  port: 5434
  username: admin
  password: admin123
  database: opende
  ssl: false

worker:
  replicas: 2

webapp:
  ingress:
    enabled: false

temporal:
  enabled: true

keycloak:
  enabled: false
monitoring:
  enabled: false
```

This connects Airbyte to your Docker-based PostgreSQL and sets scaling options.

---

## 🚀 Step 4: Install Airbyte

```bash
abctl local install --values ~/openDE/open-data-engineering/airbyte-values.yaml
```

This sets up:

* A `kind` Kubernetes cluster
* All Airbyte services (webapp, server, worker, temporal)

Allow 5–15 minutes.

---

## 🌍 Step 5: Access Airbyte UI

Open:

```
http://localhost:8000
```

Or:

```
http://<your-vm-ip>:8000
```

Complete onboarding by entering email/org name.

---

## 🔁 Step 6: Start/Stop Lifecycle

To **stop (destroy)**:

```bash
abctl local uninstall
```

To **restart** (with data preserved):

```bash
abctl local install --values ~/openDE/open-data-engineering/airbyte-values.yaml
```

✅ Since PostgreSQL is external (in Docker), your data persists across reinstalls.

---

## 🧠 Tips

### Use Aliases:

```bash
echo "alias airbyte-up='abctl local install --values ~/openDE/open-data-engineering/airbyte-values.yaml'" >> ~/.bashrc
echo "alias airbyte-down='abctl local uninstall'" >> ~/.bashrc
source ~/.bashrc
```

### Scale Airbyte Workers:

In `airbyte-values.yaml`:

```yaml
worker:
  replicas: 3
```

---

## ✅ You're Production-Ready 🎉

Your Airbyte is now:

* ✔️ Durable (external Postgres)
* ✔️ Scalable (replicas)
* ✔️ Restart-safe
* ✔️ Kubernetes-native (future-proof)

### Optional Next Steps:

* Add MinIO or S3 for log/state persistence
* Enable Prometheus & Grafana monitoring
* Secure with Ingress + TLS

Let this be your foundation for a modern open-source data stack.