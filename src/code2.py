# ============================================
# WRO 2026 Future Engineers - Team RoboTronics
# Obstacle Challenge - Main Program
# Robot: LEGO Spike Prime
# Firmware: LEGO MINDSTORMS Robot Inventor
# Version: 1.0 - EN DESARROLLO
# Estado: Pendiente de pruebas con pilares reales
# Ultima modificacion: Septiembre 2026
# ============================================

from hub import port, button, sound
import sys
import time

sys.path.append('/projects')
from pyhuskylens.pyhuskylens import HuskyLens, ALGORITHM_COLOR_RECOGNITION

VELOCIDAD_TRACCION = 80
VELOCIDAD_DIRECCION = 60
GIRO_SUAVE = 15
GIRO_PILAR = 40
MARGEN_CENTRO = 50
TIEMPO_GIRO = 80
TIEMPO_CENTRO = 60
TIEMPO_ESPERA = 6000

NARANJA = -1
AZUL = 3

esquinas = 0
mi_giro = None
bloqueado = False
tiempo_bloqueo = 0

hl = HuskyLens('C', 9600, debug=True)
time.sleep_ms(2000)

if hl.knock():
    hl.set_alg(ALGORITHM_COLOR_RECOGNITION)
    print("Camara OK")
else:
    print("Camara ERROR")
    sound.beep(220, 1000, 100)

sound.beep(440, 200, 100)
while not button.left.is_pressed():
    time.sleep_ms(100)

sound.beep(880, 200, 100)
time.sleep_ms(500)

port.F.motor.run_at_speed(VELOCIDAD_TRACCION)
time.sleep_ms(2000)

while esquinas < 12:

    color_raw = port.A.device.get()
    dist_izq_raw = port.D.device.get()
    dist_der_raw = port.E.device.get()

    color_visto = color_raw[0] if color_raw else None
    dist_izq = dist_izq_raw[0] if (dist_izq_raw and dist_izq_raw[0] is not None) else None
    dist_der = dist_der_raw[0] if (dist_der_raw and dist_der_raw[0] is not None) else None

    ahora = time.ticks_ms()

    # Leer camara
    bloques = hl.get_blocks()
    pilar_rojo = False
    pilar_verde = False
    pilar_x = 160  # centro de la imagen

    for b in bloques:
        if b.ID == 1:
            pilar_rojo = True
            pilar_x = b.x
        elif b.ID == 2:
            pilar_verde = True
            pilar_x = b.x

    if bloqueado and time.ticks_diff(ahora, tiempo_bloqueo) > TIEMPO_ESPERA:
        bloqueado = False

    # PRIORIDAD 1 - Pilar rojo → pasar por la derecha
    if pilar_rojo:
        if pilar_x > 160:
            port.B.motor.run_at_speed(-GIRO_PILAR)
        else:
            port.B.motor.run_at_speed(GIRO_PILAR)

    # PRIORIDAD 2 - Pilar verde → pasar por la izquierda
    elif pilar_verde:
        if pilar_x < 160:
            port.B.motor.run_at_speed(GIRO_PILAR)
        else:
            port.B.motor.run_at_speed(-GIRO_PILAR)

    # PRIORIDAD 3 - Naranja → esquina
    elif color_visto == NARANJA and not bloqueado:
        bloqueado = True
        tiempo_bloqueo = time.ticks_ms()

        if mi_giro is None:
            mi_giro = 'DERECHA'
            print("Sentido: HORARIO")
            sound.beep(660, 100, 100)

        if mi_giro == 'DERECHA':
            port.B.motor.run_at_speed(VELOCIDAD_DIRECCION)
        else:
            port.B.motor.run_at_speed(-VELOCIDAD_DIRECCION)

        time.sleep_ms(TIEMPO_GIRO)

        if mi_giro == 'DERECHA':
            port.B.motor.run_at_speed(-VELOCIDAD_DIRECCION)
        else:
            port.B.motor.run_at_speed(VELOCIDAD_DIRECCION)

        time.sleep_ms(TIEMPO_CENTRO)
        port.B.motor.run_at_speed(0)

        esquinas += 1
        print("Esquina: " + str(esquinas))

    # PRIORIDAD 4 - Azul → ruedas rectas
    elif color_visto == AZUL:
        port.B.motor.run_at_speed(0)

    # PRIORIDAD 5 - Sin color → centrado entre paredes
    else:
        if dist_izq is not None and dist_der is not None:
            diferencia = dist_izq - dist_der
            if diferencia > MARGEN_CENTRO:
                port.B.motor.run_at_speed(GIRO_SUAVE)
            elif diferencia < -MARGEN_CENTRO:
                port.B.motor.run_at_speed(-GIRO_SUAVE)
            else:
                port.B.motor.run_at_speed(0)
        else:
            port.B.motor.run_at_speed(0)

    time.sleep_ms(50)


port.F.motor.run_at_speed(0)
port.B.motor.run_at_speed(0)
sound.beep(880, 500, 100)
print("FIN")