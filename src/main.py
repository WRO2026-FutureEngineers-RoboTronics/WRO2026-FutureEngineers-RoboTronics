# WRO 2026 Future Engineers - Team RoboTronics
# Open Challenge - Main Program
# Robot: LEGO Spike Prime
# Firmware: LEGO MINDSTORMS Robot Inventor
# Version: 3.0

import sys
sys.path.append('/projects')

from hub import port, button, display
import time

# =====================
# CONFIGURACION
# =====================

VELOCIDAD_TRACCION = 80
VELOCIDAD_DIRECCION = 50
GIRO_SUAVE = 30
MARGEN_CENTRO = 50

# =====================
# VARIABLES
# =====================

esquinas = 0
mi_giro = None
ultimo_color = None

# =====================
# PROGRAMA PRINCIPAL
# =====================

# Esperar boton izquierdo
display.show(display.Image.ARROW_W)
while not button.is_pressed('left'):
    time.sleep_ms(100)

display.show(display.Image.GO_RIGHT)
time.sleep_ms(500)

# Arrancar traccion
port.F.motor.run_at_speed(VELOCIDAD_TRACCION)

# =====================
# BUCLE PRINCIPAL
# =====================

while esquinas < 12:

    # Leer sensores
    color_visto = port.A.device.get()
    dist_izq = port.D.device.get()
    dist_der = port.E.device.get()

    print("C:" + str(color_visto) + " I:" + str(dist_izq) + " D:" + str(dist_der) + " E:" + str(esquinas))

    # PRIORIDAD 1 - Color = esquina
    if color_visto != ultimo_color:
        ultimo_color = color_visto

        if color_visto and (color_visto[0] in [3, 7]):
            color_actual = color_visto[0]

            if mi_giro is None:
                if color_actual == 7:
                    mi_giro = 'DERECHA'
                    display.show(display.Image.ARROW_E)
                else:
                    mi_giro = 'IZQUIERDA'
                    display.show(display.Image.ARROW_W)

            if mi_giro == 'DERECHA':
                port.B.motor.run_at_speed(VELOCIDAD_DIRECCION)
            else:
                port.B.motor.run_at_speed(-VELOCIDAD_DIRECCION)

            esquinas += 1
            display.show(str(esquinas))

    # PRIORIDAD 2 - Centrado entre paredes
    else:
        if dist_izq and dist_der:
            diferencia = dist_izq[0] - dist_der[0]
            if diferencia > MARGEN_CENTRO:
                port.B.motor.run_at_speed(GIRO_SUAVE)
            elif diferencia < -MARGEN_CENTRO:
                port.B.motor.run_at_speed(-GIRO_SUAVE)
            else:
                port.B.motor.run_at_speed(0)
        else:
            port.B.motor.run_at_speed(0)

    time.sleep_ms(50)

# =====================
# FIN
# =====================

port.F.motor.run_at_speed(0)
port.B.motor.run_at_speed(0)
display.show(display.Image.YES)
