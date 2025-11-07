import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import queue
import sys
import time

import Laboratorio2 as game


class QueueWriter:
    """Redirect sys.stdout writes into a queue (for GUI polling)."""
    def __init__(self, q):
        self.q = q

    def write(self, msg):
        if msg:
            self.q.put(msg)

    def flush(self):
        pass


def create_gui():
    root = tk.Tk()
    root.title('Clash Fight')

    # Banner / encabezado creativo
    banner = tk.Frame(root, bg='#2b2b2b')
    banner.pack(fill=tk.X)

    title_lbl = tk.Label(banner, text='Clash Fight', fg='white', bg='#2b2b2b',
                         font=('Helvetica', 28, 'bold'))
    title_lbl.pack(padx=12, pady=(12, 0))

    subtitle = tk.Label(banner, text='¡Batalla de héroes épica!', fg='#ffd24d', bg='#2b2b2b',
                        font=('Helvetica', 12, 'italic'))
    subtitle.pack(padx=12, pady=(0, 12))

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    text = ScrolledText(frame, width=80, height=25)
    text.pack(fill=tk.BOTH, expand=True)

    control_frame = tk.Frame(root)
    control_frame.pack(fill=tk.X, padx=8, pady=(0, 8))

    rounds_var = tk.IntVar(value=5)
    tk.Label(control_frame, text='Rondas:').pack(side=tk.LEFT)
    tk.Entry(control_frame, width=4, textvariable=rounds_var).pack(side=tk.LEFT, padx=(0, 8))

    # Styled Play button
    play_btn = tk.Button(control_frame, text='▶ Play', bg='#ff5c5c', fg='white',
                         activebackground='#ff7b7b', font=('Helvetica', 11, 'bold'))
    play_btn.pack(side=tk.LEFT)

    q = None
    worker_thread = None
    original_stdout = sys.stdout

    def poll_queue():
        nonlocal q, worker_thread, original_stdout
        try:
            while True:
                msg = q.get_nowait()
                if msg is None:
                    # sentinel: trabajo terminado
                    play_btn.config(state=tk.NORMAL)
                    sys.stdout = original_stdout
                    text.insert(tk.END, '\n-- Combate finalizado --\n')
                    text.see(tk.END)
                    return
                text.insert(tk.END, msg)
                text.see(tk.END)
        except queue.Empty:
            pass
        if worker_thread and worker_thread.is_alive():
            root.after(100, poll_queue)
        else:
            if sys.stdout is not original_stdout:
                sys.stdout = original_stdout
            play_btn.config(state=tk.NORMAL)

    def start_battle():
        nonlocal q, worker_thread, original_stdout
        play_btn.config(state=tk.DISABLED)
        text.delete('1.0', tk.END)
        q = queue.Queue()
        original_stdout = sys.stdout
        sys.stdout = QueueWriter(q)

        def worker():
            # Crear las estructuras del juego localmente (no ejecutar main de module)
            listaheroe = game.ListaHeroe()
            listaheroe.agregar_heroe("Aragorn", 10, 100, 20, "fuego")
            listaheroe.agregar_heroe("Legolas", 8, 80, 25, "agua")
            listaheroe.agregar_heroe("Gimili", 12, 70, 30, "tierra")
            listaheroe.agregar_heroe("Tron", 15, 90, 30, "agua")

            listaturno = game.ListaCircularTurnos()
            listaturno.agregar_turnos(listaheroe)

            # Imprimir estado inicial y ejecutar combate
            listaheroe.mostrar_lista()
            listaturno.mostrar_turnoscircular()
            listaturno.recorrer(rounds_var.get(), listaheroe)
            listaheroe.heroe_mayor_PV()
            listaheroe.mostrar_lista_final()

            # marcar finalización
            q.put(None)

        worker_thread = threading.Thread(target=worker, daemon=True)
        worker_thread.start()
        root.after(100, poll_queue)

    play_btn.config(command=start_battle)

    # Mensaje inicial más creativo
    welcome = (
        "Bienvenido a Clash Fight!\n"
        "Reúne a tus héroes, pulsa Play y observa cómo se desarrolla la batalla.\n\n"
        "Consejos:\n"
        " - Ajusta el número de rondas antes de empezar.\n"
        " - Observa los efectos de los poderes (fuego/agua/tierra).\n\n"
    )
    text.insert(tk.END, welcome)
    text.insert(tk.END, 'Pulsa ▶ Play para iniciar el combate.\n')

    root.mainloop()


if __name__ == '__main__':
    create_gui()
