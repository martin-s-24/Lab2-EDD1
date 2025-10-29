import random

class NodoHeroe:
        self.nombre = nombre
        self.nivel = nivel
        self.puntosvida = puntosvida
        self.ataque = ataque
        self.next = None

class ListaHeroe:

    def __init__(self):
        self.head = None
    
    def agregar_heroe(self, nombre, nivel, puntosvida, ataque):
        nuevo_heroe = NodoHeroe(nombre, nivel, puntosvida, ataque)
        if not self.head:
            self.head = nuevo_heroe
        else:
            actual = self.head
            while actual.next:
                actual = actual.next
            actual.next = nuevo_heroe

    def eliminar_heroe(self, nombre):
        if not self.head:
            print("La lista está vacía.")
            return
        actual = self.head
        previo = None
        while actual and actual.nombre != nombre:
            previo = actual
            actual = actual.next
        if actual is None:
            print(f"No se encontró el héroe '{nombre}'.")
            return
        if previo is not None:
            previo.next = actual.next
        else:
            self.head = actual.next
        print(f"Héroe '{nombre}' eliminado correctamente.")

    def buscar_heroe(self, nombre):
        actual = self.head
        while actual:
            if actual.nombre == nombre:
                print(f"Héroe encontrado: Nombre: {actual.nombre}, Nivel: {actual.nivel}, PV: {actual.puntosvida}, Ataque: {actual.ataque}")
                return True
            actual = actual.next
        return None
    
    def mostrar_lista(self):
        if not self.head:
            print("La lista está vacía.")
            return
        actual = self.head
        while actual:
            print(f'Nombre: {actual.nombre}, Nivel: {actual.nivel}, PV: {actual.puntosvida}, Ataque: {actual.ataque}')
            actual = actual.next

    def mejorar_heroe(self, nombre, incremento_PV, incremento_ataque):
        if self.buscar_heroe(nombre) == True:
            heroe = self.head
            while heroe and heroe.nombre != nombre:
                heroe = heroe.next
            heroe.puntosvida += incremento_PV
            heroe.ataque += incremento_ataque
            print(f"Héroe '{nombre}' mejorado. PV: {heroe.puntosvida}, Ataque: {heroe.ataque}")
        else:
            print(f"No se encontró el héroe '{nombre}'.")

    def curar_heroe(self, nombre, puntos):
        heroe = self.buscar_heroe(nombre)
        if heroe:
            heroe.puntosvida += puntos
            print(f"{nombre} se curó {puntos} puntos. PV actual: {heroe.puntosvida}")
        else:
            print(f"No se encontró el héroe '{nombre}'.")

class NodoTurno:
    def __init__(self, nombre_heroe):
        self.nombre_heroe = nombre_heroe
        self.next = None

class ListaCircularTurnos:
    def __init__(self):
        self.head = None

    def agregar_turno(self, nombre_heroe):
        nuevo = NodoTurno(nombre_heroe)
        if not self.head:
            self.head = nuevo
            nuevo.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = nuevo
            nuevo.next = self.head

    def eliminar_turno(self, nombre_heroe):
        if not self.head:
            print("No hay turnos para eliminar.")
            return

        actual = self.head
        previo = None

        while True:
            if actual.nombre_heroe == nombre_heroe:
                if previo:
                    previo.next = actual.next
                else:
                    if actual.next == self.head:
                        self.head = None
                    else:
                        temp = self.head
                        while temp.next != self.head:
                            temp = temp.next
                        temp.next = actual.next
                        self.head = actual.next
                print(f"Héroe '{nombre_heroe}' eliminado de los turnos.")
                return
            previo = actual
            actual = actual.next
            if actual == self.head:
                break

    def mostrar_turnoscircular(self):
        if not self.head:
            print("La lista de turnos está vacía.")
            return
        actual = self.head
        print("\nOrden actual de turnos:")
        while True:
            print(f"- {actual.nombre_heroe}")
            actual = actual.next
            if actual == self.head:
                break

    def recorrer(self, rondas, lista_info):
        if not self.head:
            print("No hay héroes en la lista de turnos.")
            return

        for ronda in range(1, rondas + 1):
            print(f"\n=== Ronda {ronda} ===")
            actual = self.head
            contador = 0

            # este while controla una vuelta completa (por cada héroe)
            while True:
                nombre = actual.nombre_heroe
                print(f"\nTurno de {nombre}:")
                accion = random.choice(["A", "C", "P"])  # A = atacar, C = curarse, P = pasar
                print(f"Acción automática: {accion}")

                if accion == "A":
                    puntos = random.randint(5, 30)
                    print(f"{nombre} ataca con {puntos} puntos.")
                    lista_info.restar_vida_aleatoria(nombre, puntos)
                elif accion == "C":
                    puntos = random.randint(5, 30)
                    print(f"{nombre} se cura {puntos} puntos.")
                    lista_info.curar_heroe(nombre, puntos)
                else:
                    print(f"{nombre} pasa su turno.")

                actual = actual.next
                contador += 1
                if actual == self.head:
                    break

            print("\nFin de la ronda. Estado actual de los héroes:")
            lista_info.mostrar_lista()

# MAIN

listaheroe = ListaHeroe()
listaheroe.agregar_heroe("Aragorn", 10, 100, 20)
listaheroe.agregar_heroe("Legolas", 8, 80, 25)
listaheroe.mostrar_lista()
listaheroe.buscar_heroe("Aragorn")

#listaturno = ListaCircularTurnos()
#listaturno.agregar_turno("Aragorn")
#listaturno.agregar_turno("Legolas")
#listaturno.mostrar_turnoscircular()