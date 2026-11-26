# Architecture

## Runtime pipeline

1. ADB connects, captures screenshots and sends input.
2. Vision performs template matching for coarse UI state.
3. Optional OCR extracts target resource values.
4. State machine drives CONNECTING -> HOME -> ARMY -> SEARCHING -> BATTLE -> RESULT, with RECOVERY on failure.
5. Strategy scores and filters targets using loot, trophies, confidence and optional Town Hall.
6. Army exposes composition, preparation and queue primitives.
7. Attack consumes the configured unit profile and planner output.
8. SQLite stores telemetry while EventBus keeps bounded recent history.
9. FastAPI exposes runtime controls and the browser dashboard polls status/events.

## Reliability rules

- Dry-run bypasses physical ADB operations and uses deterministic target data.
- Unknown live UI is never treated as HOME.
- State timeouts prevent indefinite stalls.
- Recovery is bounded by BOT_MAX_RECOVERY.
- Runtime errors are recorded as telemetry.
- Device-specific templates and coordinates remain calibration inputs.

## Production boundary

The generic automation core is complete. Game-version/device-specific templates must be captured from the actual target environment; fabricated assets are intentionally excluded.
