# ============================================
# WRO 2026 Future Engineers - Team RoboTronics
# Open Challenge - Main Program
# Robot: LEGO Spike Prime
# Firmware: LEGO MINDSTORMS Robot Inventor
# Version: 3.2 - EN PRUEBAS
# Estado: Funciona en tapete, pendiente ajuste fino
# Ultima modificacion: Septiembre 2026
# ============================================

from hub import port, button, sound
import time

VELOCIDAD_TRACCION = 80
VELOCIDAD_DIRECCION = 60
GIRO_SUAVE = 15
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

    if color_visto == NARANJA:
        estado = "NARANJA"
    elif color_visto == AZUL:
        estado = "AZUL"
    else:
        estado = str(color_visto)

    print("C:" + estado + " BLQ:" + str(bloqueado) + " E:" + str(esquinas))

    if bloqueado and time.ticks_diff(ahora, tiempo_bloqueo) > TIEMPO_ESPERA:
        bloqueado = False

    # NARANJA → girar derecha
    if color_visto == NARANJA and not bloqueado:
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

    # AZUL → ruedas rectas
    elif color_visto == AZUL:
        port.B.motor.run_at_speed(0)

    # Sin color → centrado
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