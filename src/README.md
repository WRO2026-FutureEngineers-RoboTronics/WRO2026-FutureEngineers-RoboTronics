# Software Architecture

## Overview

Main program for LEGO Spike Prime.
Language: MicroPython (Spike 3 API)
File: main.py
Slot: 1

---

## Port Configuration

| Port | Component | Function |
|------|-----------|----------|
| A | Color sensor | Detects orange/blue lines facing down |
| B | Traction motor | Drives rear wheels forward/backward |
| C | Steering motor | Turns front wheels left/right |
| D | Distance sensor | Detects front wall |
| E | Distance sensor | Measures left wall distance |
| F | Distance sensor | Measures right wall distance |

---

## Program Phases

### Phase 1 — Direction Detection
Robot moves forward and reads color sensor.
First colored line determines driving direction:
- Orange → Clockwise → Turn RIGHT
- Blue → Counterclockwise → Turn LEFT

### Phase 2 — Lap Completion
Robot completes 3 laps using priority system:

Priority 1: Color line detected → turn and count corner
Priority 2: Front wall closer than 25cm → turn
Priority 3: Center between walls using side sensors

### Phase 3 — Stop
After 12 corners (4 x 3 laps) all motors stop.
Hub displays OK.

---

## Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| VELOCIDAD_TRACCION | 800 | Forward speed in deg/sec |
| VELOCIDAD_DIRECCION | 400 | Steering speed in deg/sec |
| GIRO_SUAVE | 200 | Gentle steering for centering |
| DISTANCIA_GIRO | 25 | Turn threshold in cm |
| MARGEN_CENTRO | 5 | Centering tolerance in cm |
| NARANJA | 7 | Color sensor value for orange |
| AZUL | 3 | Color sensor value for blue |

---

## Problems Solved

**Problem 1 — Slow movement**
run_to_absolute_position() was too slow.
Solution: motor.run() at 800 deg/sec.

**Problem 2 — Double corner counting**
Two lines per corner caused double counting.
Solution: Track last detected color, only react on change.

**Problem 3 — First corner missed**
Robot detected direction but did not turn at first corner.
Solution: Direction detection and turning unified into one event.

**Problem 4 — Variable track width**
Inner walls change position each round.
Solution: Two side distance sensors center robot automatically.

**Problem 5 — Orange not detected**
Color sensor returned -1 for orange lines.
Solution: Using RGBI mode for orange detection combined
with standard color mode for blue detection.

---

## How to Upload

1. Open LEGO Spike Prime app
2. Connect hub via USB
3. Go to Python mode
4. Copy main.py content into Slot 1
5. Press download

## How to Run

1. Press center button to turn on hub
2. Hub shows "?" — waiting for start
3. Press LEFT button to start
4. Robot detects direction automatically
5. Completes 3 laps and shows "OK"

---

## Calibration

Run this to check color sensor values:

```python
from hub import port
import color_sensor
import runloop

async def main():
    while True:
        color = color_sensor.color(port.A)
        rgbi = color_sensor.rgbi(port.A)
        print("Color:" + str(color) + " RGBI:" + str(rgbi))
        await runloop.sleep_ms(100)

runloop.run(main())
```

Place sensor over each color and note values.
Update NARANJA and AZUL constants in main.py.
