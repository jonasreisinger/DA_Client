import tkinter as tk
import asyncio
import threading
from send import send_npy_file  # Importieren Sie die Funktion send() aus Ihrem anderen Modul


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestura")
        self.root.geometry("1000x1000")

        # Initialer Zustand des Buttons
        self.is_started = False

        # Textfeld erstellen (ca. 500 Pixel breit)
        self.text_entry = tk.Entry(self.root, width=70)
        self.text_entry.place(relx=0.5, rely=0.95, anchor='center')  # Positioniert am unteren Rand, zentriert

        # Start/Stop-Button erstellen
        self.start_stop_button = tk.Button(self.root, text="Start", command=self.toggle_button)
        self.start_stop_button.place(relx=0.5, rely=0.9, anchor='center')  # Über dem Textfeld, zentriert

        # Einrichten der asyncio-Ereignisschleife in einem separaten Thread
        self.loop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(target=self.start_loop, args=(self.loop,), daemon=True)
        self.loop_thread.start()

        # Event zum Stoppen des asynchronen Tasks
        self.stop_event = asyncio.Event()

        # Schließen-Ereignis behandeln
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    # Funktion, die beim Drücken des Start-Buttons aufgerufen wird
    def on_start(self):
        self.text_entry.delete(0, tk.END)
        self.stop_event.clear()  # Sicherstellen, dass das Event zurückgesetzt ist
        # Asynchronen Task starten
        asyncio.run_coroutine_threadsafe(self.run_send(), self.loop)

    # Funktion, die beim Drücken des Stop-Buttons aufgerufen wird
    def on_stop(self):
        self.text_entry.delete(0, tk.END)
        # Stop-Event setzen, um die Schleife zu beenden
        self.stop_event.set()

    async def run_send(self):
        while not self.stop_event.is_set():
            await send_npy_file()  # Hier wird die asynchrone Funktion send() aufgerufen
            await asyncio.sleep(1)  # Eine Sekunde warten

    # Funktion zum Umschalten des Buttons
    def toggle_button(self):
        if self.is_started:
            # Wenn gestartet, stoppen
            self.is_started = False
            self.start_stop_button.config(text="Start")
            self.on_stop()
        else:
            # Wenn gestoppt, starten
            self.is_started = True
            self.start_stop_button.config(text="Stop")
            self.on_start()

    # Funktion zum sauberen Schließen der Anwendung
    def on_close(self):
        self.on_stop()  # Sicherstellen, dass die Schleife gestoppt wird
        self.loop.call_soon_threadsafe(self.loop.stop)  # Ereignisschleife stoppen
        self.loop_thread.join()  # Warten, bis der Loop-Thread beendet ist
        self.root.destroy()  # Fenster schließen


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
