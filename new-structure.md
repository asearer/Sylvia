sylvia/
├── apps/                        # Individual ML apps/microservices
│   ├── playground/              # Original ML playground
│   │   ├── src/                 # Application code
│   │   ├── notebooks/           # Experimentation notebooks
│   │   ├── data/                # Raw & processed data specific to this app
│   │   ├── models/              # Trained model checkpoints
│   │   ├── tests/
│   │   └── Dockerfile
│   │
│   ├── classifier/              # New ML app
│   │   ├── src/
│   │   ├── notebooks/
│   │   ├── data/
│   │   ├── models/
│   │   ├── tests/
│   │   └── Dockerfile
│   │
│   └── ...                      # Future apps
│
├── services/                    # Shared microservices (optional)
│   ├── auth/
│   ├── data/
│   └── ...
│
├── libs/                        # Shared libraries/utilities
│   ├── ml-utils/                # Helper functions, preprocessing, metrics
│   ├── api-clients/             # For inter-service communication
│   └── ...
│
├── experiments/                 # Global experiments, logging, dashboards
│
├── scripts/                     # Devops, deployment, orchestration scripts
│
├── docker-compose.yml           # Optional orchestration for local dev
├── README.md
└── .gitignore
