# ============================================
# WRO 2026 Future Engineers - Team RoboTronics
# Open Challenge - Main Program
# Robot: LEGO Spike Prime
# Firmware: LEGO MINDSTORMS Robot Inventor
# Version: 2.1 - FINAL
# Estado: Funciona en tapete, pendiente ajuste fino
# Ultima modificacion: Septiembre 2026
# ============================================

from hub import port, button, sound
import time

VELOCIDAD_TRACCION = 90
VELOCIDAD_DIRECCION = 65
ANGULO_GIRO = 25
ANGULO_CENTRO = 3
MARGEN_CENTRO = 12
DIF_CENTRO = 20
TIEMPO_ESPERA = 4000
TIEMPO_FINAL = 2000

esquinas = 0
mi_giro = None
bloqueado = False
tiempo_bloqueo = 0

def es_naranja():
    raw = port.A.device.get()
    if raw and len(raw) >= 5:
        r = raw[2]
        g = raw[3]
        if r is not None and g is not None and g > 0:
            return r / g > 1.5
    return False

def es_azul():
    raw = port.A.device.get()
    if raw and len(raw) >= 5:
        r = raw[2]
        b = raw[4]
        if r is not None and b is not None and r > 0:
            return b / r > 1.5
    return False

def get_distancias():
    izq = port.D.device.get()
    der = port.E.device.get()
    i = izq[0] if (izq and izq[0] is not None) else None
    d = der[0] if (der and der[0] is not None) else None
    return i, d

def centrar():
    i, d = get_distancias()
    if i is not None and d is not None:
        dif = i - d
        if dif > DIF_CENTRO + MARGEN_CENTRO:
            port.B.motor.run_to_position(ANGULO_CENTRO - 3, 20)
        elif dif < DIF_CENTRO - MARGEN_CENTRO:
            port.B.motor.run_to_position(ANGULO_CENTRO + 3, 20)
        else:
            port.B.motor.run_to_position(ANGULO_CENTRO, 20)
    else:
        port.B.motor.run_to_position(ANGULO_CENTRO, 20)

sound.beep(440, 200, 100)
while not button.left.is_pressed():
    time.sleep_ms(100)

sound.beep(880, 200, 100)
time.sleep_ms(500)

port.F.motor.run_at_speed(VELOCIDAD_TRACCION)

# FASE 1 - detectar sentido
while mi_giro is None:
    if es_naranja():
        mi_giro = 'DERECHA'
        print("Sentido: HORARIO")
        sound.beep(880, 200, 100)
    elif es_azul():
        mi_giro = 'IZQUIERDA'
        print("Sentido: ANTIHORARIO")
        sound.beep(440, 200, 100)
    time.sleep_ms(20)

# Girar en la primera esquina
port.F.motor.run_at_speed(0)
if mi_giro == 'DERECHA':
    port.B.motor.run_to_position(ANGULO_GIRO, VELOCIDAD_DIRECCION)
else:
    port.B.motor.run_to_position(-ANGULO_GIRO, VELOCIDAD_DIRECCION)

time.sleep_ms(500)
port.F.motor.run_at_speed(VELOCIDAD_TRACCION)
bloqueado = True
tiempo_bloqueo = time.ticks_ms()
esquinas = 1
print("Esquina: 1")

# FASE 2 - bucle principal
while esquinas < 12:

    naranja = es_naranja()
    azul = es_azul()
    ahora = time.ticks_ms()
    i, d = get_distancias()

    if naranja:
        estado = "NARANJA"
    elif azul:
        estado = "AZUL"
    else:
        estado = "otro"

    if i and d:
        print("C:" + estado + " I:" + str(i) + " D:" + str(d) + " DIF:" + str(i-d) + " E:" + str(esquinas))

    if bloqueado and time.ticks_diff(ahora, tiempo_bloqueo) > TIEMPO_ESPERA:
        bloqueado = False

    # SENTIDO HORARIO
    if mi_giro == 'DERECHA':

        if naranja and not bloqueado:
            bloqueado = True
            tiempo_bloqueo = time.ticks_ms()

            port.F.motor.run_at_speed(0)
            port.B.motor.run_to_position(ANGULO_GIRO, VELOCIDAD_DIRECCION)
            time.sleep_ms(500)
            port.F.motor.run_at_speed(VELOCIDAD_TRACCION)

            esquinas += 1
            print("Esquina: " + str(esquinas))

        elif azul:
            port.F.motor.run_at_speed(0)
            time.sleep_ms(200)
            port.B.motor.run_to_position(ANGULO_CENTRO, 30)
            time.sleep_ms(800)
            port.F.motor.run_at_speed(VELOCIDAD_TRACCION)
            bloqueado = False
            print("AZUL - recto")

        else:
            centrar()

    # SENTIDO ANTIHORARIO
    elif mi_giro == 'IZQUIERDA':

        if azul and not bloqueado:
            bloqueado = True
            tiempo_bloqueo = time.ticks_ms()

            port.F.motor.run_at_speed(0)
            port.B.motor.run_to_position(-ANGULO_GIRO, VELOCIDAD_DIRECCION)
            time.sleep_ms(500)
            port.F.motor.run_at_speed(VELOCIDAD_TRACCION)

            esquinas += 1
            print("Esquina: " + str(esquinas))

        elif naranja:
            port.F.motor.run_at_speed(0)
            time.sleep_ms(200)
            port.B.motor.run_to_position(ANGULO_CENTRO, 30)
            time.sleep_ms(800)
            port.F.motor.run_at_speed(VELOCIDAD_TRACCION)
            bloqueado = False
            print("NARANJA - recto")

        else:
            centrar()

    time.sleep_ms(20)

# FASE 3 - fin, seguir recto hasta zona de salida
port.F.motor.run_at_speed(0)
port.B.motor.run_to_position(ANGULO_CENTRO, 30)
time.sleep_ms(500)

port.F.motor.run_at_speed(VELOCIDAD_TRACCION)
time.sleep_ms(TIEMPO_FINAL)

port.F.motor.run_at_speed(0)
port.B.motor.run_to_position(ANGULO_CENTRO, 30)
sound.beep(880, 500, 100)
print("FIN")