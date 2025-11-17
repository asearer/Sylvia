# Sylvia: From Playground to Event-Driven ML Platform

**Sylvia** began as a personal ML playground, but is now a **mono-repo of independent ML microservices**, orchestrated through Matrix event-driven architecture. Each app, dashboard, and bot is self-contained, modular, and Dockerized — sharing common libraries and infrastructure.

---

## Matrix Event Integration

- All ML apps and dashboards communicate via **Matrix rooms** (using `libs/api-clients/matrix_wrapper.py`).
- Event types: `ml.metrics`, `ml.status`, `ml.model`, and more.
- Dashboards and bots receive and orchestrate events for full decoupled, event-driven ML workflows.

**Main components:**
- `apps/classifier/src/train.py` — ML training example, sends structured events.
- `libs/api-clients/matrix_wrapper.py` — Matrix event client wrapper (sync/async, modular).
- `experiments/dashboards/metrics_dashboard.ipynb` — Dashboard that receives/visualizes Matrix events.
- `services/matrix/src/bot.py` — Example orchestration bot (listens/responds to events/commands).

See code comments for environment variable configuration for Matrix homeserver, user, password, and room IDs.

---

## Project Structure & Modularity

- Every ML app, dashboard, library, and bot has its own `tests/` folder — **no top-level `tests/` directory**.
- Modern structure: 
    - `apps/<app>/tests/` for ML apps
    - `libs/api-clients/tests/` for wrappers/libraries
    - `services/matrix/tests/` for bots
    - `experiments/dashboards/tests/` for dashboards
- **All tests use `pytest`** (and `pytest-mock`/`unittest.mock` for external services).
- All Matrix, file, and network dependencies are mocked for fast, isolated, repeatable CI/dev runs.

**How to discover tests (from repo root):**
```sh
pytest apps/classifier/tests/
pytest libs/api-clients/tests/
pytest experiments/dashboards/tests/
pytest services/matrix/tests/
# Also:
pytest apps/playground/tests/
pytest apps/personality-engine/tests/
pytest apps/sylvia_app/tests/
```

---

## Docker & Orchestration

- **Every service/app includes a Dockerfile** and is composed via `docker-compose.yml`.
- Matrix config is via environment variables (env file, secrets or Compose overrides).
- For interactive dashboard, run the Jupyter service and access on port 8888.
- Orchestrate services with:

```sh
docker-compose --profile experimental up
```

- To test Docker builds and basic starts:
```sh
bash scripts/test_docker_smoke.sh
```

---

## Running Tests

- Tests cover ML workflows, Matrix communication (including error/negative cases), dashboard event parsing, bot command orchestration, and Docker smoke/health.
- `conftest.py` in each test directory provides fixtures for mock credentials, Matrix clients, and events.
- Example test invocation:

```sh
pytest apps/classifier/tests/       # ML training/tests
pytest libs/api-clients/tests/      # Matrix wrapper/tests
pytest experiments/dashboards/tests/# Dashboard event/tests
pytest services/matrix/tests/       # Bot event/tests
```

---

## Extending the Platform
- To add a new app, dashboard, or bot: create a new folder with its own `src/` and `tests/`.
- Import and use the shared Matrix wrapper (do not implement Matrix integration yourself).
- Standardize new event types and room assignments in code comments and docs.

---

*Sylvia is an evolving, experiment-friendly, event-driven ML ecosystem: modular, scalable, Dockerized, and fully testable across all components.*
