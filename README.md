# ISHClansOfClashBot

Full-stack Python automation framework for Clash of Clans using ADB, OpenCV template matching, optional Tesseract OCR, a state machine, target scoring, attack control, SQLite persistence, FastAPI and a browser dashboard.

## Architecture

```
Android / Emulator -> ADB -> Vision + OCR -> State Machine
                                      |-> Army
                                      |-> Strategy
                                      |-> Attack
                                      -> SQLite
                                      -> FastAPI + Web UI
```

## Implemented

- ADB device discovery, screenshots, taps, swipes and back navigation.
- Dry-run mode without an Android device.
- OpenCV template matching.
- Optional Tesseract OCR.
- Explicit runtime states and recovery path.
- Configurable target scoring and loot thresholds.
- Async runtime with event history.
- SQLite event persistence.
- FastAPI API and dashboard.
- WebSocket event stream.
- Unit tests for persistence, runtime lifecycle and target scoring.

## Setup

Python 3.11+:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m bot
```

Windows PowerShell:

```powershell
.venv\\Scripts\\Activate.ps1
```

The dashboard is served by the application at the configured host/port.

## Configuration

Copy `.env.example` to `.env`.

Key settings:

- `BOT_DRY_RUN=true`: no ADB device required; uses a deterministic simulated target.
- `BOT_DEVICE_SERIAL`: optional ADB serial.
- `BOT_SCREEN_WIDTH` / `BOT_SCREEN_HEIGHT`: emulator resolution.
- `BOT_SCREENSHOT_INTERVAL`: state-machine tick interval.
- `BOT_DATABASE_URL`: SQLite database URL.
- `BOT_TEMPLATE_DIR`: state-template directory.
- `BOT_OCR_ENABLED`: enable Tesseract OCR.
- `BOT_OCR_LANG`: OCR language.

## Templates

For live device operation, add calibrated templates:

```
assets/templates/
  home.png
  army.png
  attack.png
  result.png
```

Templates are device/resolution dependent and are intentionally not fabricated.

## API

- `GET /api/health`
- `GET /api/status`
- `GET /api/devices`
- `GET /api/events?limit=50`
- `POST /api/start`
- `POST /api/stop`
- `WS /ws/events`

## Validation boundary

The repository now contains the executable application structure and unit tests, but live game interaction still requires device-specific visual calibration. The GitHub Actions CI workflow is intentionally left for the final step, as requested.
