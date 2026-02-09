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
| **"List models"** | Lists all available local LLM models found in the `/models` directory. | List of model names |
| **"Current model"** | Reports which LLM is currently loaded and active. | Active model name |
| **"Switch to [name]"** | Unloads the current model and loads the specified model. | Confirmation message |

## Usage
Speak these commands clearly into the microphone (if Voice STT is active) or type them into the **Dashboard Chat**.

*Note: The system uses simple keyword matching. Phrases containing these keywords (e.g., "Sylvia, what is your **status**?") will triggering the command.*
