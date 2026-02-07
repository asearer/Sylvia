# Avatar Integration

The **Avatar Bridge** service allows Sylvia to control a 3D avatar (e.g., in Unity or Unreal Engine).

## Connection

The Avatar Bridge starts a WebSocket server on `ws://localhost:8765`.

## Protocol

Messages are JSON strings.

### From System -> Avatar

```json
{
  "type": "viseme",
  "payload": {
    "viseme_id": 12,
    "duration": 0.2
  }
}
```

```json
{
  "type": "emotion",
  "payload": {
    "emotion": "happy",
    "intensity": 0.8
  }
}
```

### From Avatar -> System

```json
{
  "type": "status",
  "payload": "ready"
}
```

## Unity Implementation Guide

1. Create a WebSocket client in Unity (using `NativeWebSocket` or similar).
2. Connect to `ws://localhost:8765`.
3. Listen for incoming JSON messages.
4. Parse `viseme` and `emotion` events to drive blend shapes or animations.
