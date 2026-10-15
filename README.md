# Jenkins automation example

Small Python project with a **declarative Jenkins pipeline** that checks out code, installs dependencies, runs tests, packages artifacts, and optionally simulates deploy.

## What's included

| File | Purpose |
|------|---------|
| `Jenkinsfile` | Multibranch / Pipeline job definition |
| `app/main.py` | Sample application code |
| `tests/` | Pytest suite consumed in CI |
| `docker-compose.yml` | Run Jenkins locally on port 8080 |

## Pipeline stages

1. **Checkout** — SCM checkout (Git)
2. **Setup** — Python venv + `pip install -r requirements.txt`
3. **Test** — `pytest`
4. **Package** — tarball archived as a Jenkins artifact
5. **Deploy** — runs only when parameter `DEPLOY_ENV` is not `none`
6. **Smoke** — quick import/run check (toggle with `RUN_SMOKE`)

Build parameters:

- `DEPLOY_ENV`: `none` | `staging` | `production`
- `RUN_SMOKE`: run post-build smoke test (default: on)

## Run tests locally (no Jenkins)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v tests/
```

## Run Jenkins locally

```bash
docker compose up -d --build
```

The image is built from `Dockerfile`, which installs `python3` and still starts Jenkins via the default image entrypoint. Do **not** replace `command` with only `apt-get install` — that runs install and exits with code 0 without starting Jenkins.

1. Open [http://localhost:8080](http://localhost:8080)
2. Get the initial admin password:

   ```bash
   docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```

3. Install suggested plugins, create an admin user.
4. **New Item** → **Pipeline** (or **Multibranch Pipeline** if this repo is on Git).
5. Under **Pipeline**, set **Definition** to *Pipeline script from SCM*, point at this repo, script path `Jenkinsfile`.
6. With this Compose setup, **Python 3** is already on `PATH` as `python3` inside the container.

### Multibranch tip

For GitHub/GitLab, use a **Multibranch Pipeline** job so each branch/PR gets its own run from the same `Jenkinsfile`.

## CI without Docker

Install Jenkins on a VM or use an existing controller; create a **Pipeline** job and paste or reference this `Jenkinsfile`. Label agents with Python 3 available.

## Extending this example

- Add a **Docker** agent (`agent { docker { image 'python:3.12-slim' } }`) for reproducible builds.
- Publish pytest JUnit XML: `pytest --junitxml=test-results/junit.xml` and wire the `junit` step in the Test stage.
- Replace the Deploy stage with SSH, Kubernetes, or cloud deploy plugins.
