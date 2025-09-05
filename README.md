# Sylvia: From Playground to Platform

**Sylvia** started as a personal ML playground for learning, but it's evolving into a **mono-repo of independent ML microservice apps**. Each app is self-contained but can share common libraries, infrastructure, and tooling.

## Repository Structure

```
sylvia/
├── apps/                  # Individual ML apps/microservices
│   ├── playground/        # Original ML playground app
│   │   ├── src/           # Application code
│   │   ├── notebooks/     # Experimentation notebooks
│   │   ├── data/          # Raw & processed data for this app
│   │   ├── models/        # Trained model checkpoints
│   │   ├── tests/
│   │   └── Dockerfile
│   ├── classifier/        # New ML app
│   │   ├── src/
│   │   ├── notebooks/
│   │   ├── data/
│   │   ├── models/
│   │   ├── tests/
│   │   └── Dockerfile
│   └── ...                # Future apps
│
├── services/              # Shared microservices (optional)
├── libs/                  # Shared utilities and helper libraries
├── experiments/           # Global experiment tracking/logging
├── scripts/               # Deployment, orchestration, and maintenance scripts
├── docker-compose.yml     # Optional local dev orchestration
├── README.md
└── .gitignore
```

## Features & Goals

* 🧩 **Modular Apps:** Each app is isolated and can evolve independently.

* 🔄 **Shared Utilities:** Avoid code duplication and promote reusability.

* 🚀 **Scalable:** Add new ML apps easily while maintaining clean structure.

* 📊 **Experiment-Friendly:** Notebooks, data, and models are organized per app for reproducibility.

## Next Steps

* Migrating the original playground app into the new structure.

* Adding new ML apps as independent services.

* Implementing shared services and libraries to streamline development.

---

*Sylvia is moving from a single app to a full ecosystem of ML tools — modular, scalable, and experiment-ready.*
