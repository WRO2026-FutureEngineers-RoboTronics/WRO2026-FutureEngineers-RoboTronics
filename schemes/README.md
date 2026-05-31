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

*Team RoboTronics — Basurto, Bilbao, Basque Country, Spain*
*WRO 2026 Future Engineers*
