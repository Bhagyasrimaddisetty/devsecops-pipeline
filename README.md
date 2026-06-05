# DevSecOps CI/CD Security Pipeline

A production-style DevSecOps pipeline that integrates automated security gates into every stage of the CI/CD process. Built with GitHub Actions, Docker, Trivy, OWASP ZAP, and Python.

---

## Architecture

```
Push to main
     │
     ▼
┌─────────────────┐
│  Stage 1        │  Python secret scanner — blocks hardcoded credentials,
│  Secret Scan    │  API keys, AWS keys, private keys before they reach repo
└────────┬────────┘
         │ pass
         ▼
┌─────────────────┐
│  Stage 2        │  pytest unit tests — 5 tests covering all API endpoints,
│  Unit Tests     │  error handling, and edge cases
└────────┬────────┘
         │ pass
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────────────┐
│Stage 3 │ │ Stage 4        │  Trivy scans container image for CVEs (exits
│Trivy   │ │ OWASP ZAP DAST │  on CRITICAL). ZAP scans live app for OWASP
│Scan    │ │ Scan           │  Top 10 vulnerabilities. Both run in parallel.
└────┬───┘ └───────┬────────┘
     │             │ pass
     └──────┬──────┘
            ▼
     ┌─────────────┐
     │  Stage 5    │  Deploys only when ALL security gates pass.
     │  Deploy     │  Blocked automatically on any failure.
     └─────────────┘
```

---

## Security Gates

| Gate | Tool | Blocks On |
|---|---|---|
| Secret Detection | Custom Python scanner | Hardcoded passwords, API keys, AWS credentials, private keys |
| Container CVE Scan | Trivy | CRITICAL severity vulnerabilities in image layers |
| DAST Scan | OWASP ZAP | Active web application vulnerabilities (OWASP Top 10) |
| Unit Tests | pytest | Failing application logic before security scans run |

---

## Project Structure

```
devsecops-pipeline/
├── app/
│   ├── app.py              # Flask REST API (4 endpoints)
│   └── requirements.txt    # Python dependencies
├── tests/
│   └── test_app.py         # 5 unit tests (pytest)
├── scripts/
│   └── secret_scanner.py   # Custom secret detection script
├── .github/
│   └── workflows/
│       └── devsecops-pipeline.yml   # Full CI/CD pipeline definition
├── Dockerfile              # Hardened container (non-root user, slim base)
└── .gitignore
```

---

## Application — REST API Endpoints

The sample application is an Asset Management API:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/assets` | List all assets |
| GET | `/assets/<id>` | Get asset by ID |
| POST | `/assets` | Create new asset |

---

## Docker Security Hardening

The Dockerfile applies the following security practices:

- **Non-root user** — application runs as `appuser`, not root
- **Slim base image** — `python:3.11-slim` reduces attack surface vs full image
- **No-cache pip install** — avoids stale cached packages
- **Minimal layers** — reduces image size and CVE exposure

```bash
# Build and run locally
docker build -t devsecops-demo .
docker run -p 5000:5000 devsecops-demo

# Test
curl http://localhost:5000/health
curl http://localhost:5000/assets
```

---

## Secret Scanner

The custom Python scanner (`scripts/secret_scanner.py`) detects:

- Hardcoded passwords and API keys
- AWS Access Key IDs (`AKIA...`)
- AWS Secret Access Keys
- Private keys (RSA, EC, OpenSSH)
- Generic tokens and secrets

```bash
# Run locally
python scripts/secret_scanner.py
```

---

## Run Locally

```bash
# Clone
git clone https://github.com/Bhagyasrimaddisetty/devsecops-pipeline
cd devsecops-pipeline

# Install dependencies
pip install -r app/requirements.txt

# Run application
python app/app.py

# Run tests
pytest tests/ -v

# Run secret scanner
python scripts/secret_scanner.py
```

---

## Pipeline in Action

Every `git push` to `main` triggers the full pipeline automatically.

View live pipeline runs: [Actions tab](../../actions)

The ZAP DAST scan report is uploaded as a downloadable artifact on every run.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python / Flask | REST API application |
| GitHub Actions | CI/CD orchestration |
| Docker | Containerisation with security hardening |
| Trivy | Container image vulnerability scanning |
| OWASP ZAP | Dynamic application security testing (DAST) |
| pytest | Unit testing |
| Custom Python | Secret detection and dependency auditing |

---

## Key Concepts Demonstrated

- Shift-left security — security checks run before deployment, not after
- Policy-as-code — pipeline blocks on security failures automatically
- Defense in depth — multiple independent security layers (SAST + DAST + container scan)
- Principle of least privilege — container runs as non-root user
- Secure SDLC — security integrated at every stage of development lifecycle
