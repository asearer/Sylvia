# Sylvia: From Playground to Platform

**Sylvia** started as a personal ML playground for learning, but it's evolving into a **mono-repo of independent ML microservice apps**. Each app is self-contained but can share common libraries, infrastructure, and tooling.

## Usage Instructions

Sylvia can be launched using **CLI**, **GUI**, or an **API backend** (future integration). Currently, a **stub backend** is available for safe testing.

### Command-Line Interface (CLI)

```bash
# Launch CLI with the stub backend
python main.py --mode cli --backend stub
```

**CLI Features:**

* `/switch [profile]` — switch active personality profile

* `/hybrid [profile:weight,...]` — set weighted hybrid personalities

* `+` / `-` — provide feedback for last response

* `exit` — quit the CLI

* Save conversations interactively after each message

### Graphical User Interface (GUI)

```bash
# Launch GUI with the stub backend
python main.py --mode gui --backend stub
```

**GUI Features:**

* Send messages to Sylvia via a chat box

* Switch personality profiles or set hybrid weights

* Debug logs and response times displayed in real-time

* Stubbed visualization panel (Matplotlib) showing placeholder data

### API (Planned)

* Uvicorn-powered API for remote interaction: `python main.py --mode api`

* Provides REST endpoints for sending messages and switching profiles

* Full model integration coming in future updates

## Features & Goals

* 🧩 **Modular Apps:** Each app is isolated and can evolve independently.

* 🔄 **Shared Utilities:** Avoid code duplication and promote reusability.

* 🚀 **Scalable:** Add new ML apps easily while maintaining clean structure.

* 📊 **Experiment-Friendly:** Notebooks, data, and models are organized per app for reproducibility.

* 💬 **Interactive Interfaces:** CLI and GUI allow real-time interaction with SylviaBot.

* 🧪 **Safe Testing:** Stubbed backend returns canned responses and prevents runtime errors from the full Personality engine or plotting issues.

## Next Steps

* Re-integrate the full Personality engine and advanced model backends.

* Enable Matplotlib-based visualization in GUI with live personality updates.

* Expand CLI/API backends for local and remote models.

* Add more ML apps and microservices while maintaining modularity.

## Running Tests

All major components include automated tests using `pytest`. Tests use `pytest-mock` or standard `unittest.mock` for Matrix communication and environment emulation.

**To run all tests for the project:**

```sh
pytest apps/classifier/tests/
pytest libs/api-clients/tests/
pytest experiments/dashboards/tests/
pytest services/matrix/tests/
```

- `conftest.py` in each test folder provides fixtures (dummy credentials, mock Matrix clients, events).
- Tests cover model, Matrix wrapper (sync/async), dashboard, and event-driven bot orchestration.
- All Matrix network operations are mocked—no real traffic expected.
- For Docker verification, use compose and `docker-compose logs` after container startup to check for errors/smoke test failures.

**Test Categories**
- `test_*.py`: Unit and integration tests (look for test_train.py, test_matrix_wrapper.py, test_dashboard.py, test_bot.py)
- Use `-k` to run specific groups of tests, e.g. `pytest ... -k 'integration'`

---

*Sylvia is moving from a single experimental playground to a full ecosystem of ML tools — modular, scalable, interactive, and experiment-ready.*
