import pygame
import random
from Laboratorio2 import ListaHeroe, ListaCircularTurnos

# Inicialización de pygame
pygame.init()
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Batalla de Héroes")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Fuente
fuente = pygame.font.SysFont("Arial", 24)
fuente_grande = pygame.font.SysFont("Arial", 48)

# Crear las listas
listaheroe = ListaHeroe()
listaheroe.agregar_heroe("Aragorn", 10, 85, 20, "fuego")
listaheroe.agregar_heroe("Legolas", 8, 80, 25, "agua")
listaheroe.agregar_heroe("Gimili", 12, 70, 30, "tierra")
listaheroe.agregar_heroe("Tron", 15, 90, 30, "agua")

listaturno = ListaCircularTurnos()
listaturno.agregar_turnos(listaheroe)

# Variables de control
reloj = pygame.time.Clock()
ejecutando = True
ronda = 1
accion_actual = ""
mensaje = ""

# Turnos
turno = listaturno.head
primer_turno = turno.nombre_heroe  # para saber cuándo vuelve al inicio


# Función para dibujar los héroes en pantalla
def dibujar_heroes():
    ventana.fill(BLANCO)
    y = 100
    actual = listaheroe.head
    while actual:
        # Color de la barra de vida
        color_barra = VERDE if actual.puntosvida > 0 else ROJO
        barra_vida = pygame.Rect(400, y, max(actual.puntosvida, 0) * 2, 20)
        pygame.draw.rect(ventana, color_barra, barra_vida)

        # Resaltar héroe en turno
        if actual.nombre == turno.nombre_heroe:
            texto = fuente.render(f"> {actual.nombre} ({actual.poder}) - PV: {actual.puntosvida}", True, AZUL)
        else:
            texto = fuente.render(f"{actual.nombre} ({actual.poder}) - PV: {actual.puntosvida}", True, NEGRO)

        ventana.blit(texto, (50, y))
        actual = actual.next
        y += 60

    # Mostrar info general
    texto_ronda = fuente.render(f"Ronda: {ronda}", True, NEGRO)
    ventana.blit(texto_ronda, (600, 30))
    texto_accion = fuente.render(accion_actual, True, AZUL)
    ventana.blit(texto_accion, (50, 30))
    texto_mensaje = fuente.render(mensaje, True, NEGRO)
    ventana.blit(texto_mensaje, (50, 500))
    pygame.display.flip()


# Función para mostrar el ganador final
def mostrar_ganador():
    ganador = None
    mayor_pv = -1
    actual = listaheroe.head
    while actual:
        if actual.puntosvida > mayor_pv:
            mayor_pv = actual.puntosvida
            ganador = actual.nombre
        actual = actual.next

    texto_final = fuente_grande.render("¡Fin del combate!", True, ROJO)
    texto_ganador = fuente.render(f"El ganador es {ganador} con {mayor_pv} PV.", True, NEGRO)
    ventana.blit(texto_final, (220, 350))
    ventana.blit(texto_ganador, (250, 420))
    pygame.display.flip()
    pygame.time.delay(4000)


# Bucle principal
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:  # Espacio = ejecutar un turno

                # 🔹 Verificar fin de combate antes del turno
                vivos = 0
                actual = listaheroe.head
                while actual:
                    if actual.puntosvida > 0:
                        vivos += 1
                    actual = actual.next
                if ronda > 5 or vivos <= 1:
                    mensaje = "¡Fin del combate!"
                    accion_actual = ""
                    dibujar_heroes()
                    mostrar_ganador()
                    ejecutando = False
                    break

                # Si la lista de turnos quedó vacía, terminar
                if not listaturno.head:
                    mensaje = "No hay más turnos. Fin."
                    mostrar_ganador()
                    ejecutando = False
                    break

                # Asegurarse de que 'turno' siempre apunte a algo válido
                if turno is None:
                    turno = listaturno.head

                nombre = turno.nombre_heroe
                accion = random.choice(["A", "C", "P"])
                accion_actual = f"Turno de {nombre} - Acción: {accion}"

                if accion == "A":
                    heroe_atacado = listaturno.atacar_heroe_aleatorio(nombre, listaheroe)
                    if heroe_atacado is None:
                        mensaje = f"{nombre} no encontró objetivo."
                    else:
                        daño = listaheroe.calcular_daño(nombre, heroe_atacado)
                        mensaje = f"{nombre} ataca a {heroe_atacado} con {daño} de daño"
                        derrotado = listaheroe.restar_vida_aleatoria(heroe_atacado, daño)
                        if derrotado:
                            removed = listaturno.eliminar_turno(heroe_atacado)
                            # actualizar referencias si se eliminó
                            if removed:
                                # si la lista quedó vacía, terminar partida
                                if not listaturno.head:
                                    mensaje = "¡Fin del combate! (todos los turnos eliminados)"
                                    dibujar_heroes()
                                    mostrar_ganador()
                                    ejecutando = False
                                    break
                                # si 'turno' apuntaba al eliminado, moverlo al head actual
                                if turno and turno.nombre_heroe == heroe_atacado:
                                    turno = listaturno.head
                                # actualizar primer_turno (opcional)
                                primer_turno = listaturno.head.nombre_heroe
                elif accion == "C":
                    puntos = random.randint(5, 30)
                    listaheroe.curar_heroe(nombre, puntos)
                    mensaje = f"{nombre} se cura {puntos} puntos."
                else:
                    mensaje = f"{nombre} pasa su turno."

                # avanzar el turno si la partida sigue
                if ejecutando and listaturno.head:
                    # si 'turno' no está en la lista actual (por eliminación), reubicarlo
                    # lo más sencillo: si turno.nombre_heroe no existe en la lista, poner turno = listaturno.head
                    existe_turno = False
                    temp = listaturno.head
                    while True:
                        if temp.nombre_heroe == turno.nombre_heroe:
                            existe_turno = True
                            break
                        temp = temp.next
                        if temp == listaturno.head:
                            break
                    if not existe_turno:
                        turno = listaturno.head
                    else:
                        turno = turno.next

                    # 🔹 Incrementar ronda cuando volvemos al head actual
                    if listaturno.head and turno == listaturno.head:
                        ronda += 1

                dibujar_heroes()

    dibujar_heroes()
    reloj.tick(30)

pygame.quit()