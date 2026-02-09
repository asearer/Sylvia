# Sylvia Voice Commands

This document lists the available voice commands for the Sylvia system.

## Core Commands

| Command Keyword | Description | Response Type |
| :--- | :--- | :--- |
| **"Hello"** / **"Hi"** | simple greeting to verify the agent is listening. | Random greeting string |
| **"Status"** | Checks the health of the Agent Core and connected services. | System status report |
| **"Time"** | Asks for the current local time. | Current time (e.g., "It is currently 06:45 PM") |
| **"Sing"** | Triggers a singing response to test the Text-to-Speech (TTS) engine's modulation. | A short song lyric |

## LLM Commands
*Requires valid `.gguf` models in the `models/` directory.*

| Command Keyword | Description | Response Type |
| :--- | :--- | :--- |
| **"List models"** | Lists all available local LLM models with their **Safety Profile**. | List of models + [Uncensored/Guarded] tags |
| **"Current model"** | Reports active model and **Safe Mode** status. | Active model + Safe Mode (ON/OFF) |
| **"Switch to [name]"** | Hot-swaps the active model. Blocked if unsafe in Safe Mode. | Confirmation or Security Alert |

## Usage
Speak these commands clearly into the microphone (if Voice STT is active) or type them into the **Dashboard Chat**.

*Note: The system uses simple keyword matching. Phrases containing these keywords (e.g., "Sylvia, what is your **status**?") will triggering the command.*
