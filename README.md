# ISHClansOfClashBot

Full-stack Python automation framework for Clash of Clans using ADB, OpenCV template matching, optional Tesseract OCR, a state machine, target scoring, attack control, SQLite persistence, FastAPI and a browser dashboard.

## Finalized components

- Async ADB client with discovery, screenshots and input primitives.
- Deterministic dry-run mode without an Android device.
- OpenCV template matching and optional Tesseract OCR.
- Explicit state machine with state timeout and bounded recovery.
- Configurable loot, confidence and Town Hall filters.
- Army composition/queue primitives and attack planning.
- SQLite event persistence and bounded in-memory history.
- FastAPI health/status/device/event/start/stop endpoints.
- Responsive polling dashboard.
- Unit tests for input, persistence, runtime lifecycle, strategy and army queue behavior.

## Setup

Python 3.11+:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    python -m bot

Windows PowerShell:

    .venv\\Scripts\\Activate.ps1

## Live-device calibration

Live operation is calibration-driven. Add templates captured from the exact emulator/device profile:

    assets/templates/
      home.png
      army.png
      attack.png
      result.png

Coordinates in .env must match the configured resolution. Unknown live UI is routed to recovery rather than assumed to be HOME.

## Configuration

Copy .env.example to .env. Important controls are BOT_DRY_RUN, BOT_DEVICE_SERIAL, BOT_SCREEN_WIDTH/HEIGHT, BOT_TEMPLATE_DIR, BOT_OCR_ENABLED/BOT_OCR_LANG, BOT_MIN_SCORE, BOT_MIN_GOLD, BOT_MIN_ELIXIR, BOT_MIN_DARK, BOT_MAX_TOWN_HALL, BOT_MAX_RECOVERY, BOT_ATTACK_UNIT_NAME/COUNT/SLOT and calibrated input coordinates.

## API

- GET /api/health
- GET /api/status
- GET /api/devices
- GET /api/events?limit=50
- POST /api/start
- POST /api/stop

The dashboard polls the API; there is no WebSocket dependency.

## Validation boundary

The application layer is finalized on the feature branch. External validation still requires the actual target emulator/device and calibrated visual assets. GitHub Actions CI is intentionally left as the final separate step.
