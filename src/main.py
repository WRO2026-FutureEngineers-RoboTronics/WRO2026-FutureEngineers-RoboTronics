# WRO 2026 Future Engineers - Team RoboTronics
# Open Challenge - Main Program
# Robot: LEGO Spike Prime
# Version: 2.0

from hub import light_matrix, port, button
import motor
import color_sensor
import distance_sensor
import runloop

# =====================
# CONFIGURACION
# =====================

VELOCIDAD_TRACCION = 800
VELOCIDAD_DIRECCION = 400
GIRO_SUAVE = 200

DISTANCIA_GIRO = 25
MARGEN_CENTRO = 5

# Valores sensor de color
AZUL = 3

# Umbrales RGBI para naranja
# R alto, G bajo, B bajo
NARANJA_R_MIN = 400
NARANJA_G_MAX = 200
NARANJA_B_MAX = 200

# =====================
# VARIABLES
# =====================

esquinas = 0
mi_giro = None
ultimo_color = None

# =====================
# FUNCIONES
# =====================

async def girar_derecha():
    motor.run(port.C, VELOCIDAD_DIRECCION)

async def girar_izquierda():
    motor.run(port.C, -VELOCIDAD_DIRECCION)

async def recto():
    motor.stop(port.C)

async def avanzar():
    motor.run(port.B, VELOCIDAD_TRACCION)

async def parar():
    motor.stop(port.B)
    motor.stop(port.C)

def detectar_naranja():
    rgbi = color_sensor.rgbi(port.A)
    r = rgbi[0]
    g = rgbi[1]
    b = rgbi[2]
    return r > NARANJA_R_MIN and g < NARANJA_G_MAX and b < NARANJA_B_MAX

def detectar_color():
    # Detecta azul con modo color normal
    # Detecta naranja con modo RGBI
    color = color_sensor.color(port.A)
    if color == AZUL:
        return 'AZUL'
    if detectar_naranja():
        return 'NARANJA'
    return None

# =====================
# PROGRAMA PRINCIPAL
# =====================

async def main():
    global esquinas, mi_giro, ultimo_color

    # Esperar boton de inicio
    await light_matrix.write("?")
    while not button.pressed(button.LEFT):
        await runloop.sleep_ms(100)

    await light_matrix.write("GO")
    await runloop.sleep_ms(500)

    await avanzar()

    # =====================
    # BUCLE PRINCIPAL
    # =====================
    while esquinas < 12:

        color_visto = detectar_color()
        dist_frontal = distance_sensor.distance(port.D)
        dist_izq = distance_sensor.distance(port.E)
        dist_der = distance_sensor.distance(port.F)

        print("C:" + str(color_visto) + " F:" + str(dist_frontal) + " I:" + str(dist_izq) + " D:" + str(dist_der) + " E:" + str(esquinas))

        # =====================
        # PRIORIDAD 1 - Color = esquina
        # =====================
        if color_visto != ultimo_color:
            ultimo_color = color_visto

            if color_visto == 'NARANJA' or color_visto == 'AZUL':

                if mi_giro is None:
                    if color_visto == 'NARANJA':
                        mi_giro = 'DERECHA'
                        await light_matrix.write("H")
                    else:
                        mi_giro = 'IZQUIERDA'
                        await light_matrix.write("A")

                if mi_giro == 'DERECHA':
                    await girar_derecha()
                else:
                    await girar_izquierda()

                esquinas += 1
                await light_matrix.write(str(esquinas))

        # =====================
        # PRIORIDAD 2 - Pared frontal
        # =====================
        elif dist_frontal and dist_frontal < DISTANCIA_GIRO:
            if mi_giro is None:
                await recto()
            elif mi_giro == 'DERECHA':
                await girar_derecha()
            else:
                await girar_izquierda()

        # =====================
        # PRIORIDAD 3 - Centrado
        # =====================
        else:
            if dist_izq and dist_der:
                diferencia = dist_izq - dist_der
                if diferencia > MARGEN_CENTRO:
                    motor.run(port.C, GIRO_SUAVE)
                elif diferencia < -MARGEN_CENTRO:
                    motor.run(port.C, -GIRO_SUAVE)
                else:
                    await recto()
            else:
                await recto()

        await runloop.sleep_ms(50)

    # =====================
    # FIN
    # =====================
    await parar()
    await light_matrix.write("OK")

runloop.run(main())
