# WRO 2026 Future Engineers — RoboTronics

## Team RoboTronics — Basurto, Bilbao, Spain

We are three siblings from Bilbao competing in 
WRO 2026 Future Engineers for the first time, 
after several years in WRO RoboMission.

| Member | Age | Role |
|--------|-----|------|
| Sandra García Arias | 20 | Programming and Strategy |
| Oscar García Arias | 16 | Mechanics and Programming |
| Asier García Arias | 16 | Programming and Testing |
| Coach: Edu | — | Guidance and Support |

---

## Our WRO History

| Year | Category | Result |
|------|----------|--------|
| 2023 | RoboMission Junior | 1st place Euskadi, Top 15 National |
| 2024 | RoboMission Senior | 2nd place Euskadi |
| 2026 | Future Engineers | Qualified for nationals |

---

## The Robot

Built with LEGO Spike Prime with HuskyLens AI camera.
The robot drives autonomously on a 3x3 meter track,
completing 3 laps and stopping in the finish section.

**Platform**: LEGO Spike Prime
**Firmware**: LEGO MINDSTORMS Robot Inventor
**Challenges**: Open Challenge + Obstacle Challenge
**Sensors**: Color sensor + 2 distance sensors + HuskyLens camera
**Motors**: 1 traction + 1 steering (Ackermann)

---

## Documentation

| Section | Content |
|---------|---------|
| [Mobility and Mechanical Design](src/README.md) | Chassis, steering, drive system |
| [Power and Sensor Architecture](schemes/README.md) | Sensors, connections, power |
| [Software and Strategy](src/README.md) | Code explanation, flow diagram |
| [Vehicle Photos](v-photos/README.md) | Robot from all angles |
| [Team Photos](t-photos/README.md) | Team information |
| [Performance Videos](video/README.md) | YouTube demonstrations |

---

## Port Configuration

| Port | Component | Function |
|------|-----------|----------|
| A | Color sensor | Detects orange/blue lines on floor |
| B | Steering motor | Turns front wheels left/right |
| C | HuskyLens camera | Detects red/green pillars |
| D | Distance sensor | Measures left wall distance |
| E | Distance sensor | Measures right wall distance |
| F | Traction motor | Drives rear wheels forward/backward |

---

## Quick Start — Open Challenge

1. Install pyhuskylens library on hub (see schemes/README.md)
2. Open LEGO MINDSTORMS Robot Inventor app
3. Upload src/open_challenge.py to hub
4. Press center button to turn on
5. Press left button to start
6. Robot completes 3 laps automatically

## Quick Start — Obstacle Challenge

1. Turn on HuskyLens and select Color Recognition mode
2. Point at RED pillar and press learn button (ID 1)
3. Point at GREEN pillar and press learn button (ID 2)
4. Upload src/obstacle_challenge.py to hub
5. Press center button to turn on
6. Press left button to start

---

## Why LEGO Spike Prime

We chose LEGO Spike Prime because we already had
the kit from our previous WRO RoboMission seasons.
This allowed us to focus our time and budget on
learning autonomous navigation rather than on
acquiring new hardware.

The Spike Prime platform provides:
- Reliable MicroPython programming environment
- Built-in rechargeable battery
- Native color and distance sensors
- Sufficient ports for our sensor configuration
- Easy mechanical construction with LEGO pieces

---

## Mechanical Design Summary

### The Main Challenge
The competition rules prohibit differential drive
systems (one motor per side). We had to build a
proper 4-wheeled car with Ackermann steering,
which is the same system used in real cars.

### Our Solution
- **Traction motor (Port F)**: drives both rear
  wheels through a shared axle connected by LEGO
  gears. Both wheels always move together.
- **Steering motor (Port B)**: moves both front
  wheels simultaneously using an Ackermann linkage
  built with LEGO Technic pieces.

### Design Iterations
**Version 1**: Simple chassis without proper
Ackermann geometry. Turning was inconsistent.

**Version 2**: Redesigned front axle with proper
steering linkage. Consistency improved significantly.

**Version 3**: Current version with optimized
sensor placement, HuskyLens camera and better
weight distribution.

---

## Software Summary

### Two Programs

**Program 1 — Open Challenge**
Uses color sensor and distance sensors only.
No camera needed. Completes 3 laps autonomously.

**Program 2 — Obstacle Challenge**
Uses HuskyLens camera to detect red and green pillars.
Passes red pillars on the right and green on the left.
Completes 3 laps and stops in finish section.

### How the Robot Navigates

**Phase 1 — Direction Detection**
The robot moves forward and reads the color sensor.
The first colored line on the track determines the
driving direction for the entire round:
- Orange first → Clockwise → Turn RIGHT at corners
- Blue first → Counterclockwise → Turn LEFT at corners

**Phase 2 — Lap Completion**
Priority system every 50ms:

Priority 1 (Obstacle only): HuskyLens detects pillar
→ steer to correct side to pass it safely.

Priority 2: Color sensor detects a line → turn and
count corner. After 12 corners (4 x 3 laps) → stop.

Priority 3: Side sensors keep robot centered between
walls by comparing left and right distances.

**Phase 3 — Stop**
After 12 corners all motors stop and hub shows OK.

---

## HuskyLens Integration

### Why we added a camera
The Obstacle Challenge requires detecting red and
green pillars placed randomly on the track. The LEGO
color sensor only detects colors at 10cm range which
is too short to react in time.

### HuskyLens solution
The HuskyLens AI camera detects colors from 50-100cm
giving enough time to adjust the robot trajectory.

### Connection
HuskyLens connects via SPIKE-OpenMV breakout board
by Anton's Mindstorms. The board generates stable 5V
from the hub battery to power the camera.

| HuskyLens cable | Breakout Board pin |
|----------------|-------------------|
| Red | 3V3 |
| Black | GND |
| Green | RX |
| Blue | TX |

Baudrate: 9600 — Protocol: Serial 9600

### Firmware change required
SPIKE 3 firmware does not support serial UART
communication with external devices. We changed
to LEGO MINDSTORMS Robot Inventor firmware which
supports the pyhuskylens library.

---

## Key Engineering Decisions

**Problem: Variable track width**
Inner walls change position each round. Fixed turns
would not work reliably.
Solution: Two side distance sensors measure both
walls and adjust steering automatically.

**Problem: Slow motor response**
run_to_absolute_position() was too slow.
Solution: motor.run() at high speed in deg/sec.

**Problem: Double corner counting**
Each corner has two colored lines close together.
Solution: Track last detected color, only react
when color changes.

**Problem: HuskyLens not connecting**
SPIKE 3 firmware incompatible with pyhuskylens.
Solution: Changed to MINDSTORMS Robot Inventor
firmware and set HuskyLens to Serial 9600 baud.

**Problem: HuskyLens power instability**
HuskyLens firmware 0.5+ draws more current.
Solution: SPIKE-OpenMV breakout board generates
stable 5V from hub battery.

---

## Constraints and Tradeoffs

| Constraint | Decision | Tradeoff |
|-----------|----------|----------|
| No differential drive | Ackermann steering | More complex mechanics |
| Only 6 Spike ports | 2 motors + 3 sensors + camera | All ports used |
| SPIKE 3 incompatible | Changed to Robot Inventor | Different programming environment |
| HuskyLens power hungry | SPIKE-OpenMV breakout board | Extra hardware needed |
| First year in category | Simple reliable approach | Less points but more consistent |

---

## How to Reproduce This Robot

### Hardware Required
- 1x LEGO Spike Prime kit (standard grey/yellow box)
- 1x LEGO Spike color sensor
- 2x LEGO Spike distance sensors
- 2x LEGO Spike large motors
- 1x HuskyLens AI camera (DFRobot)
- 1x SPIKE-OpenMV breakout board (Anton's Mindstorms)
- LEGO Technic pieces for chassis

### Firmware Setup
1. Download LEGO MINDSTORMS Robot Inventor app
2. Connect hub via USB
3. Update hub to Robot Inventor firmware

### Library Installation
1. Go to github.com/antonsmindstorms/pyhuskylens
2. Open installer/install_pyhuskylens.py
3. Click Raw → Copy all content
4. Paste in new MINDSTORMS Python program
5. Open console [>_] → Click Play
6. Wait for SUCCESS message
7. Reinstall after every hub firmware update

### Calibration
Run this to check color sensor values:

```python
import sys
sys.path.append('/projects')
from hub import port
import time

while True:
    color = port.A.device.get()
    print("Color: " + str(color))
    time.sleep_ms(200)
```

Place sensor over orange and blue lines.
Note the values and update constants in code.

---

## Current Version — v2.0

### What changed from v1.0
- Added HuskyLens camera for Obstacle Challenge
- Changed firmware to MINDSTORMS Robot Inventor
- Added SPIKE-OpenMV breakout board
- Two separate programs for each challenge

### Development Timeline

| Phase | Status | Description |
|-------|--------|-------------|
| v1.0 Mechanics | ✅ Done | Ackermann chassis with Spike |
| v1.0 Open Challenge | ✅ Done | 3 laps with color + distance |
| v1.0 Testing | ✅ Done | Tested at provincial competition |
| Provincial competition | ✅ Done | Qualified for nationals |
| v2.0 Camera research | ✅ Done | HuskyLens selected |
| v2.0 Firmware change | ✅ Done | Robot Inventor firmware |
| v2.0 Camera connected | ✅ Done | Serial 9600 working |
| v2.0 Obstacle Challenge | 🔄 In progress | Testing with pillars |
| National competition | 📅 Planned | September 12-13 2026 |

---

## Lessons Learned

### What we underestimated
- Mechanical complexity of Ackermann steering with LEGO
- SPIKE 3 firmware incompatible with external UART devices
- HuskyLens firmware 0.5+ requires 9600 baud only
- Library must be reinstalled after every hub update

### What worked well
- LEGO Spike as base platform saved time and budget
- Color + distance sensor combination for corner detection
- HuskyLens detects pillars from 50-100cm reliably
- SPIKE-OpenMV breakout board solves power issues

### What we would do differently
- Start with Robot Inventor firmware from the beginning
- Research UART compatibility before buying camera
- Build practice track at home from day one

---

*Team RoboTronics — Basurto, Bilbao, Basque Country, Spain*
*WRO 2026 Future Engineers 2026*
