import tkinter as tk
from tkinter import ttk
import time

from config import APP_NAME, VERSION, ALWAYS_ON_TOP, START_ARMED
from safety import SafetyCore
from screen import get_screen_size, get_cursor_position
import cursor


class MennoGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{VERSION}")
        self.root.geometry("430x330")
        self.root.minsize(390, 280)
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)

        if ALWAYS_ON_TOP:
            self.root.attributes("-topmost", True)

        self.safety = SafetyCore(self.root)
        self.safety.set_status_callback(self.set_status)
        self.safety.set_stop_callback(self.on_emergency_stop)

        self._build_style()
        self._build_ui()

        if not START_ARMED:
            self.set_status("Menno staat uit.")
        else:
            self.safety.start()

        self.update_hardware_info()

    def _build_style(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", font=("Segoe UI", 9))
        style.configure("Card.TFrame", relief="solid", borderwidth=1)
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"))
        style.configure(
            "Danger.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(14, 10),
        )

    def _build_ui(self):
        outer = ttk.Frame(self.root, padding=16)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x")

        ttk.Label(header, text="MENNO", style="Title.TLabel").pack(side="left")
        ttk.Label(
            header,
            text=f"LOCAL MANAGER • v{VERSION}",
            style="Sub.TLabel",
        ).pack(side="right", pady=7)

        card = ttk.LabelFrame(outer, text="Status", padding=12)
        card.pack(fill="x", pady=(14, 10))

        self.status_var = tk.StringVar(value="Menno wordt gestart...")
        self.status_label = ttk.Label(
            card,
            textvariable=self.status_var,
            wraplength=360,
        )
        self.status_label.pack(anchor="w")

        self.info_var = tk.StringVar(value="")
        ttk.Label(card, textvariable=self.info_var).pack(
            anchor="w", pady=(10, 0)
        )

        buttons = ttk.Frame(outer)
        buttons.pack(fill="x", pady=(0, 10))

        ttk.Button(
            buttons,
            text="Cursorpositie vernieuwen",
            command=self.update_hardware_info,
            style="Action.TButton",
        ).pack(fill="x", pady=3)

        ttk.Button(
            buttons,
            text="Test cursor → midden van scherm",
            command=self.test_cursor_move,
            style="Action.TButton",
        ).pack(fill="x", pady=3)

        # Large red emergency button.
        danger_frame = ttk.Frame(outer)
        danger_frame.pack(side="bottom", fill="x")

        self.stop_button = tk.Button(
            danger_frame,
            text="🔴  MENNO AFSLUITEN / NOODSTOP",
            command=lambda: self.safety.trigger_emergency_stop("rode knop"),
            bg="#c62828",
            fg="white",
            activebackground="#8e0000",
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            bd=0,
            padx=12,
            pady=12,
            cursor="hand2",
        )
        self.stop_button.pack(fill="x")

        ttk.Label(
            danger_frame,
            text="Noodstop: 3x ESC binnen 1,5 seconde.",
            style="Sub.TLabel",
        ).pack(pady=(5, 0))

    def set_status(self, message: str):
        self.root.after(
            0,
            lambda: self.status_var.set(str(message))
        )

    def on_emergency_stop(self, reason: str):
        try:
            self.stop_button.configure(
                text=f"🛑 NOODSTOP — {reason}",
                bg="#6d0000",
                activebackground="#6d0000",
            )
        except tk.TclError:
            pass

    def update_hardware_info(self):
        width, height = get_screen_size()
        x, y = get_cursor_position()
        self.info_var.set(
            f"Scherm: {width} × {height} px    |    Cursor: X={x}, Y={y}"
        )

        if not self.safety.is_stopped():
            self.set_status("Menno actief • safety core actief")

    def test_cursor_move(self):
        if self.safety.is_stopped():
            self.set_status("Actie geweigerd: Menno staat uit.")
            return

        width, height = get_screen_size()
        if width <= 0 or height <= 0:
            self.set_status("Schermgrootte kon niet worden bepaald.")
            return

        self.set_status("Cursor wordt naar het midden van het scherm bewogen...")
        self.root.update_idletasks()

        x = width // 2
        y = height // 2

        try:
            ok = cursor.move_to(x, y, duration=0.2, safety=self.safety)
        except Exception as exc:
            self.set_status(f"Cursorfout: {exc}")
            return

        if ok:
            self.update_hardware_info()
            self.set_status("Cursor staat in het midden. Safety core blijft actief.")
        else:
            self.set_status("Cursoractie gestopt door safety core.")

    def shutdown(self):
        self.safety.request_normal_shutdown()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    MennoGUI().run()
