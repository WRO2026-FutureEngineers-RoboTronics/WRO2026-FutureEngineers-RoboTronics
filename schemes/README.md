# Power and Sensor Architecture

## Power System

The robot runs entirely on the LEGO Spike Prime 
rechargeable battery (7.2V Li-Ion). No external 
power source is needed. The Spike hub distributes 
power to all motors and sensors through its ports.

---

## Port Configuration

| Port | Component | Direction | Purpose |
|------|-----------|-----------|---------|
| A | Large motor | — | Steering front wheels left/right |
| B | Large motor | — | Driving rear wheels forward/backward |
| C | Color sensor | Facing DOWN | Detects orange/blue floor lines |
| D | Distance sensor | Facing FORWARD | Detects front wall for corner turns |
| E | Distance sensor | Facing LEFT | Measures left wall distance |
| F | Distance sensor | Facing RIGHT | Measures right wall distance |

---

## Sensor Placement Decisions

**Color Sensor — Port C — Facing down**
Mounted at the front of the robot pointing toward 
the floor. Placed at the front (not underneath) 
so it detects lines earlier, giving the robot 
more time to react before the corner.

**Front Distance Sensor — Port D — Facing forward**
Mounted at the front center. Acts as backup 
corner detection when the color sensor misses 
a line. Triggers a turn when wall is closer 
than 25cm.

**Left Distance Sensor — Port E — Facing left**
Mounted on the left side. Measures distance to 
the left wall continuously. Used together with 
the right sensor to keep the robot centered.

**Right Distance Sensor — Port F — Facing right**
Mounted on the right side. Measures distance to 
the right wall continuously. Used together with 
the left sensor to keep the robot centered.

---

## Why Three Distance Sensors

The Open Challenge randomizes inner wall positions 
each round. Track width varies between 600mm and 
1000mm. Using two side sensors allows the robot 
to adapt to any configuration automatically by 
measuring both walls and adjusting steering to 
maintain equal distances on both sides.

The front sensor adds a safety layer for corner 
detection independent of floor color detection.

---

## Connection Photo

[Photo to be added]
