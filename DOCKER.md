# Docker & Deployment

Sylvia is designed to run as a set of Docker containers.

## Services

| Service | Build Path | Description |
|---------|------------|-------------|
| `agent-core` | `services/agent_core/Dockerfile` | Main logic |
| `voice-stt` | `services/voice_stt/Dockerfile` | Speech Recognition |
| `voice-tts` | `services/voice_tts/Dockerfile` | Speech Synthesis |
| `avatar-bridge` | `services/avatar_bridge/Dockerfile` | Avatar Connection |
| `redis` | `redis:alpine` | Message Bus |

## Running with Docker Compose

To start the full stack:

```bash
docker-compose up --build
```

### Environment Variables

Containers use environment variables for configuration.
- `REDIS_HOST`: Hostname of Redis server (default: `redis`)
- `REDIS_PORT`: Port of Redis server (default: `6379`)

### Audio Device Mapping

To use host audio devices (Microphone/Speakers) inside Docker containers on Linux:
The `docker-compose.yml` maps `/dev/snd:/dev/snd`.

**Note for Mac/Windows**: Direct audio device mapping is challenging. 
- The services are configured to fall back to **Simulation Mode** if audio devices are not found.
- In Simulation Mode:
  - STT simulates user input periodically.
  - TTS logs audio playback instead of playing sound.
