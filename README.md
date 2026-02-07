# Sylvia: Advanced AI Agent Platform

Sylvia is a professional-grade, modular, and containerized AI agent platform designed for multi-modal interaction (Voice, Avatar, Tools).

## Architecture

The system is decomposed into specialized microservices that communicate via Redis Pub/Sub:

- **Agent Core**: The brain (Reasoning, Planning, Personality).
- **Voice STT**: Speech-to-Text (Hearing).
- **Voice TTS**: Text-to-Speech (Speaking).
- **Avatar Bridge**: WebSocket bridge to Unity 3D Avatar.
- **Capabilities**: Modular tools and skills.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+ (for local development)
- Unity (for 3D Avatar)

### Building and Running

```bash
# Build all services
docker-compose build

# Start the system
docker-compose up
```

## Documentation

- [Architecture Overview](ARCHITECTURE.md)
- [Docker & Deployment Guide](DOCKER.md)
- [Avatar Integration Guide](AVATAR.md)

## Development

The project structure:
- `apps/`: Orchestration apps (UI, etc.)
- `services/`: Microservices source code
- `libs/`: Shared libraries
- `docker-compose.yml`: Local orchestraion
