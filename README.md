# Random Moving Squares (Pygame)

A simple Python + Pygame project that displays 10 colored squares moving randomly around a window.

## Features

- 10 squares spawned at random positions
- Random movement with slight direction changes
- Bounce behavior at window edges
- On-screen overlay with status and controls
- Keyboard controls for pause, reset, and speed adjustment

## Project Structure

- `main.py`: full application logic (game loop, input, drawing, movement)
- `REPORT.md`: lab/project report
- `JOURNAL.md`: interaction and change log

## Requirements

- Python 3.10+ (project currently uses a local virtual environment)
- `pygame`

## Setup

1. Create and activate a virtual environment (optional if already using `.venv`).
2. Install dependencies:

```powershell
pip install pygame
```

## Run

From the project root:

```powershell
python main.py
```

If you are using this project's virtual environment directly:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Controls

- `SPACE`: pause/resume animation
- `R`: reset squares to new random positions/colors/speeds
- `UP`: increase target FPS (up to 120)
- `DOWN`: decrease target FPS (down to 10)
- `ESC` or window close button: quit

## Learning Notes

This project is intentionally simple and suitable for first-year practice.

Suggested extensions:

- Show measured FPS (`clock.get_fps()`) in the overlay
- Add color randomization without position reset
- Add collision handling between squares
- Add unit tests for pure helper functions
