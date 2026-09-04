# Power and Sensor Architecture

## Power System

The robot runs on the LEGO Spike Prime rechargeable
battery (7.2V Li-Ion). The SPIKE-OpenMV breakout board
generates stable 5V from the hub battery to power the
HuskyLens camera. No external battery is needed.

---

## Port Configuration

| Port | Component | Direction | Purpose |
|------|-----------|-----------|---------|
| A | Color sensor | Facing DOWN | Detects orange/blue floor lines |
| B | Steering motor | — | Turns front wheels left/right |
| C | HuskyLens camera | Facing FORWARD | Detects red/green pillars |
| D | Distance sensor | Facing LEFT | Measures left wall distance |
| E | Distance sensor | Facing RIGHT | Measures right wall distance |
| F | Traction motor | — | Drives rear wheels forward/backward |

---

## HuskyLens Connection

The HuskyLens connects to the Spike hub via the
SPIKE-OpenMV breakout board by Anton's Mindstorms.

| HuskyLens cable | Breakout Board pin |
|----------------|-------------------|
| Red | 3V3 |
| Black | GND |
| Green | RX |
| Blue | TX |

**Baudrate**: 9600
**Protocol**: Serial 9600
**Breakout board**: SPIKE-OpenMV by Anton's Mindstorms

The breakout board generates stable 5V from the hub
battery. This is necessary because HuskyLens firmware
0.5+ draws more current than the 3V3 pin can supply.

---

## Sensor Placement Decisions

**Color Sensor — Port A — Facing down**
Mounted at the front of the robot pointing toward the
floor. Placed at the front (not underneath) so it
detects lines earlier, giving the robot more time to
react before the corner.

**HuskyLens Camera — Port C — Facing forward**
Mounted at the front of the robot facing forward.
Detects red and green pillars from 50-100cm distance.
This gives enough time to adjust trajectory before
reaching the pillar.

**Left Distance Sensor — Port D — Facing left**
Mounted on the left side. Measures distance to the
left wall continuously. Used together with the right
sensor to keep the robot centered between walls.

**Right Distance Sensor — Port E — Facing right**
Mounted on the right side. Measures distance to the
right wall continuously. Used together with the left
sensor to keep the robot centered between walls.

---

## Why Two Distance Sensors Instead of Three

In the original design we had three distance sensors
(front, left, right). After adding the HuskyLens camera
in Port C we removed the front sensor since the camera
takes that port.

The front distance sensor is no longer needed because:
- The color sensor detects corners reliably
- The camera provides additional forward awareness
- Two side sensors are sufficient for wall centering

---

## Why HuskyLens Instead of Color Sensor for Pillars

The LEGO Spike color sensor only detects colors at
approximately 10cm range. At competition speed this
is too short to react and adjust trajectory safely.

The HuskyLens detects colors from 50-100cm giving
enough time to plan and execute the avoidance maneuver.

---

## Firmware and Library

**Hub firmware**: LEGO MINDSTORMS Robot Inventor
SPIKE 3 firmware does not support serial UART
communication with external devices. Robot Inventor
firmware is required for HuskyLens communication.

**Library**: pyhuskylens
Install after every hub firmware update:
1. Go to github.com/antonsmindstorms/pyhuskylens
2. Open installer/install_pyhuskylens.py
3. Click Raw → Copy all
4. Paste in MINDSTORMS Python program
5. Open console [>_] → Play → wait for SUCCESS

---

## Connection Photo

![Connection](https://drive.google.com/uc?export=view&id=16hHux8NCgSVoiMJ4zjoonzMYlw9nv1yy)
