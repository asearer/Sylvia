sylvia/
├── apps/                  # Individual microservice apps
│   ├── playground/        # Original ML playground app
│   │   ├── src/
│   │   ├── tests/
│   │   └── Dockerfile
│   ├── classifier/        # Example: new ML app
│   │   ├── src/
│   │   ├── tests/
│   │   └── Dockerfile
│   └── ...                # Future apps
│
├── services/              # Shared microservices (if needed)
│   ├── auth/              # Authentication service
│   ├── data/              # Shared data handling service
│   └── ...                # Other shared services
│
├── libs/                  # Shared libraries/utilities
│   ├── ml-utils/
│   ├── api-clients/
│   └── ...                
│
├── scripts/               # Devops, deployment, maintenance scripts
│
├── docker-compose.yml     # Optional: orchestrate multi-service dev environment
├── README.md
└── .gitignore
