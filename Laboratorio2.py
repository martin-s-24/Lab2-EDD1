import random

class NodoHeroe:
    def __init__(self, nombre, nivel, puntosvida, ataque, poder):
        self.nombre = nombre
        self.nivel = nivel
        self.puntosvida = puntosvida
        self.ataque = ataque
        self.poder = poder
        self.next = None

class ListaHeroe:

    def __init__(self):
        self.head = None
    
    def agregar_heroe(self, nombre, nivel, puntosvida, ataque, poder):
        while poder != "fuego" and poder != "agua" and poder != "tierra":
            poder = input("Ingrese un poder válido (fuego, agua, tierra): ")
        nuevo_heroe = NodoHeroe(nombre, nivel, puntosvida, ataque, poder)
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
                print(f"Héroe encontrado: Nombre: {actual.nombre}, Nivel: {actual.nivel}, PV: {actual.puntosvida}, Ataque: {actual.ataque}, Poder: {actual.poder}")
                return True
            actual = actual.next
        return None
    
    def mostrar_lista(self):
        if not self.head:
            print("La lista está vacía.")
            return
        actual = self.head
        while actual:
            print(f'Nombre: {actual.nombre}, Nivel: {actual.nivel}, PV: {actual.puntosvida}, Ataque: {actual.ataque}, Poder: {actual.poder}')
            actual = actual.next

    def mejorar_heroe(self, nombre, incremento_PV, incremento_ataque):
        if self.buscar_heroe(nombre):
            heroe = self.head
            while heroe and heroe.nombre != nombre:
                heroe = heroe.next
            heroe.puntosvida += incremento_PV
            heroe.ataque += incremento_ataque
            print(f"Héroe '{nombre}' mejorado. PV: {heroe.puntosvida}, Ataque: {heroe.ataque}")
        else:
            print(f"No se encontró el héroe '{nombre}'.")

    def curar_heroe(self, nombre, puntos):
        heroe = self.head
        while heroe and heroe.nombre != nombre:
            heroe = heroe.next
        heroe.puntosvida += puntos
        print(f"{nombre} se curó {puntos} puntos de vida. PV actual: {heroe.puntosvida}")

    def restar_vida_aleatoria(self, nombre, daño):
        heroe = self.head
        while heroe and heroe.nombre != nombre:
            heroe = heroe.next
        heroe.puntosvida -= daño
        if heroe.puntosvida < 0:
            heroe.puntosvida = 0
            print(f"{nombre} perdió {daño} puntos de vida. PV actual: {heroe.puntosvida}. {nombre} ha sido derrotado.")
            return True
        print(f"{nombre} perdió {daño} puntos de vida. PV actual: {heroe.puntosvida}")

    def heroe_mayor_PV(self):
        if not self.head:
            print("La lista está vacía.")
            return
        mayor = self.head
        actual = self.head.next
        while actual:
            if actual.puntosvida > mayor.puntosvida:
                mayor = actual
            actual = actual.next
        print(f"Héroe con mayor PV: {mayor.nombre} con {mayor.puntosvida} puntos de vida.")
    
    def mostrar_lista_final (self):
        if not self.head:
            print("La lista está vacía.")
            return
        actual = self.head
        while actual:
            if actual.puntosvida > 0:
                print(f'Nombre: {actual.nombre}, PV: {actual.puntosvida}, Estado: Vivo')
            else:
                print(f'Nombre: {actual.nombre}, PV: {actual.puntosvida}, Estado: Eliminado')
            actual = actual.next
    
    def obtener_ataque(self, nombre):
        heroe = self.head
        while heroe and heroe.nombre != nombre:
            heroe = heroe.next
        return heroe.ataque 
    
    def obtener_poder(self, nombre):
        heroe = self.head
        while heroe and heroe.nombre != nombre:
            heroe = heroe.next
        return heroe.poder
    
    def calcular_daño(self, nombre_atacante, nombre_atacado):
        daño = random.randint(5, 30) + self.obtener_ataque(nombre_atacante)
        if (self.obtener_poder(nombre_atacante) == "fuego" and self.obtener_poder(nombre_atacado) == "agua" or ):
            self.obtener_poder(nombre_atacante) == "agua" and self.obtener_poder(nombre_atacado) == "tierra" or
            self.obtener_poder(nombre_atacante) == "tierra" and self.obtener_poder(nombre_atacado) == "fuego"):
            daño /= 2
            print(f"El ataque de {nombre_atacante} ({self.obtener_poder(nombre_atacante)}) no es muy efectivo contra {nombre_atacado} ({self.obtener_poder(nombre_atacado)}). Daño reducido a la mitad.")
        return daño

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
                print(f"No se encontró el héroe '{nombre_heroe}' en los turnos.")
                return

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

    def atacar_heroe_aleatorio(self, nombre_atacante):
        actual = self.head
        while True:
            for i in range(random.randint(1, 11)): #Se escoge un número aleatorio de 1 a 10, pero podía otro rango 
                actual = actual.next
            if actual.nombre_heroe != nombre_atacante:
                return actual.nombre_heroe
        
    def recorrer(self, rondas, lista_info):
        if not self.head:
            print("No hay héroes en la lista de turnos.")
            return

        for ronda in range(1, rondas + 1):
            print(f"\n=== Ronda {ronda} ===")
            actual = self.head

            # este while controla una vuelta completa (por cada héroe)
            while True:
                nombre = actual.nombre_heroe
                print(f"\nTurno de {nombre}:")
                accion = random.choice(["A", "C", "P"])  # A = atacar, C = curarse, P = pasar
                print(f"Acción automática: {accion}")

                if accion == "A":
                    heroe_atacado = self.atacar_heroe_aleatorio(nombre)
                    daño = lista_info.calcular_daño(nombre, heroe_atacado)
                    print(f"{nombre} ataca con {daño} puntos a {heroe_atacado}.")
                    derrotado = lista_info.restar_vida_aleatoria(heroe_atacado, daño)
                    if derrotado:
                        self.eliminar_turno(nombre)
                elif accion == "C":
                    puntos = random.randint(5, 30)
                    print(f"{nombre} se cura {puntos} puntos.")
                    lista_info.curar_heroe(nombre, puntos)
                else:
                    print(f"{nombre} pasa su turno.")

                actual = actual.next
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

listaturno = ListaCircularTurnos()
listaturno.agregar_turno("Aragorn")
listaturno.agregar_turno("Legolas")
listaturno.mostrar_turnoscircular()