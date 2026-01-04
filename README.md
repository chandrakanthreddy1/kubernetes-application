# 🚀 Kubernetes Voting Application

A **production-style microservices application** deployed on **Kubernetes**, showcasing:

- Microservices communication
- Background worker pattern
- Centralized logging with **ELK**
- Monitoring with **Prometheus & Grafana**

---

## 📌 Overview

Users vote through a frontend UI.  
Votes are processed asynchronously by a worker, temporarily stored in Redis, persisted in PostgreSQL, and observed using logs and metrics.

---

## 🧱 Architecture Components

### 🔹 Application Services
- **Vote App** – Frontend UI to cast votes
- **Result App** – Frontend UI to view results
- **Worker** – Background processor
- **Redis** – In-memory vote store
- **PostgreSQL** – Persistent database

### 🔹 Observability Stack
- **Fluent Bit / Fluentd**
- **Elasticsearch**
- **Kibana**
- **Prometheus**
- **Grafana**
- **Node Exporter**
- **kube-state-metrics**

---

## 🧭 Architecture Diagram

```mermaid
flowchart LR
    User --> VoteApp
    VoteApp --> Redis[(Redis)]
    Redis --> Worker
    Worker --> Postgres[(PostgreSQL)]
    Postgres --> ResultApp
    ResultApp --> User

    subgraph Logging
        FluentBit --> Elasticsearch --> Kibana
    end

    subgraph Monitoring
        NodeExporter --> Prometheus
        KubeStateMetrics --> Prometheus
        Prometheus --> Grafana
    end
    ```