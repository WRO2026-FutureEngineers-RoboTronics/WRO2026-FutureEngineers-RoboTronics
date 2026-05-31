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
| 2026 | Future Engineers | First year |

---

## The Robot

Built with LEGO Spike Prime. The robot drives 
autonomously on a 3x3 meter track, completing 
3 laps and stopping in the finish section.

**Platform**: LEGO Spike Prime
**Challenge**: Open Challenge (3 laps autonomous)
**Sensors**: Color sensor + 3 distance sensors
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

## Quick Start

1. Connect Spike hub via USB
2. Upload src/main.py to Slot 1
3. Press center button to turn on
4. Press left button to start
5. Robot completes 3 laps automatically

---

## Port Configuration

| Port | Component | Function |
|------|-----------|----------|
| A | Motor | Steering (front wheels) |
| B | Motor | Traction (rear wheels) |
| C | Color sensor | Detects lines on floor |
| D | Distance sensor | Front wall detection |
| E | Distance sensor | Left wall distance |
| F | Distance sensor | Right wall distance |

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
- **Traction motor (Port B)**: drives both rear 
  wheels through a shared axle connected by LEGO 
  gears. Both wheels always move together.
- **Steering motor (Port A)**: moves both front 
  wheels simultaneously using an Ackermann linkage 
  built with LEGO Technic pieces.

### Design Iterations
**Version 1**: Simple chassis without proper 
Ackermann geometry. Turning was inconsistent.

**Version 2**: Redesigned front axle with proper 
steering linkage. Consistency improved significantly.

**Version 3**: Current version with optimized 
sensor placement and better weight distribution.

---

## Software Summary

### How the Robot Navigates

The program has three phases:

**Phase 1 — Direction Detection**
The robot moves forward and reads the color sensor. 
The first colored line on the track determines the 
driving direction for the entire round:
- Orange first → Clockwise → Turn RIGHT at corners
- Blue first → Counterclockwise → Turn LEFT at corners

**Phase 2 — Lap Completion**
The robot uses a priority system every 50ms:

Priority 1: Color sensor detects a line → turn and 
count corner. After 12 corners (4 x 3 laps) → stop.

Priority 2: Front distance sensor reads less than 
25cm → turn as backup if color is missed.

Priority 3: Side sensors keep robot centered between 
walls by comparing left and right distances continuously.

**Phase 3 — Stop**
After 12 corners all motors stop and hub shows OK.

### Key Engineering Decisions

**Problem: Variable track width**
The inner walls change position each round. Track 
width varies between 600mm and 1000mm. Fixed turns 
would not work reliably.
Solution: Two side distance sensors measure both 
walls and adjust steering automatically.

**Problem: Slow movement**
Initially used run_to_absolute_position() which was 
extremely slow and jerky.
Solution: Switched to motor.run() with speed in 
degrees per second (800 deg/s instead of percentage).

**Problem: Double corner counting**
Each corner has two colored lines close together. 
Robot was counting each corner twice.
Solution: Track last detected color and only react 
when color changes.

**Problem: First corner missed**
Robot detected direction but did not turn at 
the first corner.
Solution: Unified direction detection and turning 
into one single event.

---

## Sensor Architecture Summary

| Sensor | Port | Placement | Why |
|--------|------|-----------|-----|
| Color sensor | C | Front, facing down | Detects lines early before corner |
| Distance sensor | D | Front, facing forward | Backup corner detection |
| Distance sensor | E | Left side | Measures left wall distance |
| Distance sensor | F | Right side | Measures right wall distance |

The color sensor is placed at the front of the 
robot (not underneath) so it detects the colored 
lines before the robot reaches the corner, giving 
more time to react.

The two side sensors work together to keep the 
robot centered regardless of where the inner 
walls are placed each round.

---

## Competition Strategy

Given our limited time in this first Future 
Engineers season, we decided to focus on:

**Priority 1 — Open Challenge**
Complete 3 laps reliably with consistent turning 
and wall centering. Target: full score of 30 points.

**Priority 2 — Documentation**
Complete and detailed GitHub repository covering 
all five evaluation criteria. Target: 30 points.

**Priority 3 — Obstacle Challenge (if time allows)**
Add a camera (OpenMV) to detect red and green 
pillars. The camera would replace the front 
distance sensor in Port D, keeping the rest 
of the system unchanged.

This strategy allows us to guarantee a solid 
base score while leaving room to improve if 
development time allows.

---

## Constraints and Tradeoffs

| Constraint | Decision | Tradeoff |
|-----------|----------|----------|
| No differential drive | Ackermann steering | More complex mechanics but rule compliant |
| Only 6 Spike ports | 2 motors + 4 sensors | No camera for Open Challenge |
| Limited time | Open Challenge first | Obstacle Challenge attempted later |
| LEGO Spike only | Native Spike sensors | Limited sensor accuracy vs ToF sensors |
| First year in category | Simple reliable approach | Less points but more consistent |

---

## How to Reproduce This Robot

### Hardware Required
- 1x LEGO Spike Prime kit (standard grey/yellow box)
- 3x LEGO Spike distance sensors
- 1x LEGO Spike color sensor
- 2x LEGO Spike large motors
- LEGO Technic pieces for chassis

### Software Setup
1. Open LEGO Spike Prime app on computer
2. Connect Spike hub via USB
3. Go to Python programming mode
4. Copy contents of src/main.py
5. Paste into Slot 1 and download

### Calibration
Run this first to check color sensor values:

```python
from hub import port
import color_sensor
import runloop

async def main():
    while True:
        print(color_sensor.color(port.C))
        await runloop.sleep_ms(200)

runloop.run(main())
```

Place orange and blue colors under the sensor. 
Note the values and update NARANJA and AZUL 
constants in main.py accordingly.

Our values: NARANJA = 7, AZUL = 4

---

*Team RoboTronics — Basurto, Bilbao, Basque Country, Spain*
*WRO 2026 Future Engineers*
