# Software Architecture

## Overview

Two programs for LEGO Spike Prime.
Language: MicroPython (MINDSTORMS Robot Inventor API)
Firmware: LEGO MINDSTORMS Robot Inventor

---

## Port Configuration

| Port | Component | Function |
|------|-----------|----------|
| A | Color sensor | Detects orange/blue lines facing down |
| B | Steering motor | Turns front wheels left/right |
| C | HuskyLens camera | Detects red/green pillars |
| D | Distance sensor | Measures left wall distance |
| E | Distance sensor | Measures right wall distance |
| F | Traction motor | Drives rear wheels forward/backward |

---

## Program 1 — Open Challenge (open_challenge.py)

### Program Phases

**Phase 1 — Direction Detection**
Robot moves forward and reads color sensor.
First colored line determines driving direction:
- Orange → Clockwise → Turn RIGHT
- Blue → Counterclockwise → Turn LEFT

**Phase 2 — Lap Completion**
Robot completes 3 laps using priority system:

Priority 1: Color line detected → turn and count corner
Priority 2: Center between walls using side sensors

**Phase 3 — Stop**
After 12 corners (4 x 3 laps) all motors stop.
Hub displays OK.

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| VELOCIDAD_TRACCION | 800 | Forward speed in deg/sec |
| VELOCIDAD_DIRECCION | 400 | Steering speed in deg/sec |
| GIRO_SUAVE | 200 | Gentle steering for centering |
| MARGEN_CENTRO | 50 | Centering tolerance in mm |

### How to Upload

1. Open LEGO MINDSTORMS Robot Inventor app
2. Connect hub via USB
3. Create new Python program
4. Copy open_challenge.py content
5. Open console [>_] and click Play

### How to Run

1. Press center button to turn on hub
2. Hub shows ? — waiting for start
3. Press LEFT button to start
4. Robot detects direction automatically
5. Completes 3 laps and shows OK

---

## Program 2 — Obstacle Challenge (obstacle_challenge.py)

### Program Phases

**Phase 1 — Direction Detection**
Same as Open Challenge. Color sensor detects first
line and sets driving direction for entire round.

**Phase 2 — Lap Completion**
Robot completes 3 laps using priority system:

Priority 1: HuskyLens detects RED pillar (ID 1)
→ steer right to pass on the right side

Priority 1: HuskyLens detects GREEN pillar (ID 2)
→ steer left to pass on the left side

Priority 2: Color line detected → turn and count corner

Priority 3: Center between walls using side sensors

**Phase 3 — Stop**
After 12 corners all motors stop. Hub displays OK.

### HuskyLens Setup Before Each Round

1. Turn on HuskyLens
2. Select Color Recognition mode
3. Point at RED pillar → press learn button → ID 1
4. Point at GREEN pillar → press learn button → ID 2
5. Save to HuskyLens memory

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| VELOCIDAD_TRACCION | 800 | Forward speed in deg/sec |
| VELOCIDAD_DIRECCION | 400 | Steering speed in deg/sec |
| GIRO_CAMARA | 300 | Steering speed when avoiding pillar |
| GIRO_SUAVE | 200 | Gentle steering for centering |
| MARGEN_CENTRO | 50 | Centering tolerance in mm |

---

## Problems Solved During Development

**Problem 1 — Slow movement**
run_to_absolute_position() was too slow and jerky.
Solution: motor.run() at high speed in deg/sec.

**Problem 2 — Double corner counting**
Two lines per corner caused double counting.
Solution: Track last detected color, only react on change.

**Problem 3 — First corner missed**
Robot detected direction but did not turn at first corner.
Solution: Direction detection and turning unified into
one single event.

**Problem 4 — Variable track width**
Inner walls change position each round.
Solution: Two side distance sensors center robot
automatically regardless of wall position.

**Problem 5 — Orange not detected**
Color sensor returned -1 for orange lines.
Solution: Tested RGBI mode. Confirmed color values
on real competition track.

**Problem 6 — HuskyLens not connecting**
SPIKE 3 firmware incompatible with pyhuskylens library.
Solution: Changed hub firmware to LEGO MINDSTORMS
Robot Inventor which supports serial UART communication.

**Problem 7 — HuskyLens baudrate**
HuskyLens firmware 0.5+ does not support 115200 baud.
Solution: Set HuskyLens to Serial 9600 and use
baudrate=9600 in pyhuskylens library.

**Problem 8 — Library disappears after hub update**
Every hub firmware update deletes installed libraries.
Solution: Save installer script on computer and
reinstall after every hub update. Takes 1 minute.

---

## Library Installation

Install pyhuskylens after every hub firmware update:

1. Go to github.com/antonsmindstorms/pyhuskylens
2. Open installer/install_pyhuskylens.py
3. Click Raw → Copy all content
4. Paste in new MINDSTORMS Python program
5. Open console [>_] → Click Play
6. Wait for SUCCESS message

---

## Color Sensor Calibration

Run this to check color sensor values on real track:

```python
from hub import port
import time

while True:
    color = port.A.device.get()
    print("Color: " + str(color))
    time.sleep_ms(200)
```

Place sensor over each color and note values.
Update color constants in code accordingly.

---

## HuskyLens Test Code

Run this to verify HuskyLens connection:

```python
import sys
sys.path.append('/projects')

from pyhuskylens.pyhuskylens import HuskyLens, ALGORITHM_COLOR_RECOGNITION
from hub import port
import time

hl = HuskyLens(port.C, 9600)
time.sleep_ms(2000)

if hl.knock():
    print("CONNECTED!")
    hl.set_alg(ALGORITHM_COLOR_RECOGNITION)
    for i in range(20):
        blocks = hl.get_blocks()
        for b in blocks:
            print("ID:" + str(b.ID) + " x:" + str(b.x))
        time.sleep_ms(500)
else:
    print("Not connected")
```
