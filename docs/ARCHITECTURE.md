# Architecture

ADB device -> screenshot -> vision/OCR -> state detection -> strategy -> actions -> event store -> API/dashboard.

Core rules: state-driven runtime, dry-run physical input, device-specific calibration outside core logic, bounded recovery, local telemetry.

Templates and coordinates must be calibrated for the actual emulator/device resolution and game version before real input is enabled.
