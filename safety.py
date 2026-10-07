import threading
import time
import tkinter as tk

from config import ESC_WINDOW_SECONDS, ESC_PRESSES_REQUIRED


class SafetyCore:
    """
    Local safety layer.

    The AI/agent should never be able to disable this layer.
    Other Menno components can check is_stopped() before actions.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self._lock = threading.Lock()
        self._stopped = False
        self._armed = True

        self._esc_times: list[float] = []
        self._status_callback = None
        self._stop_callback = None

        self._global_listener = None

    def set_status_callback(self, callback):
        self._status_callback = callback

    def set_stop_callback(self, callback):
        self._stop_callback = callback

    def start(self) -> bool:
        """Start the global ESC listener. Returns True if available."""
        try:
            from pynput import keyboard
        except ImportError:
            self._set_status(
                "ESC noodstop: pynput ontbreekt. Installeer requirements.txt."
            )
            return False

        def on_press(key):
            if self._stopped or not self._armed:
                return

            try:
                if key != keyboard.Key.esc:
                    return
            except Exception:
                return

            now = time.monotonic()

            with self._lock:
                self._esc_times = [
                    t for t in self._esc_times
                    if now - t <= ESC_WINDOW_SECONDS
                ]
                self._esc_times.append(now)

                if len(self._esc_times) >= ESC_PRESSES_REQUIRED:
                    self._esc_times.clear()
                    self._stopped = True

            if self._stopped:
                # Always perform UI work on Tk's main thread.
                self.root.after(0, self.trigger_emergency_stop, "3x ESC")

        self._global_listener = keyboard.Listener(on_press=on_press)
        self._global_listener.daemon = True
        self._global_listener.start()

        self._set_status("Noodstop actief: druk 3x snel op ESC.")
        return True

    def is_stopped(self) -> bool:
        with self._lock:
            return self._stopped

    def is_armed(self) -> bool:
        with self._lock:
            return self._armed and not self._stopped

    def trigger_emergency_stop(self, reason: str = "rode knop"):
        """Hard local stop. This does not depend on any API."""
        with self._lock:
            already_stopped = self._stopped
            self._stopped = True
            self._armed = False
            self._esc_times.clear()

        if self._global_listener is not None:
            try:
                self._global_listener.stop()
            except Exception:
                pass

        self._set_status(f"NOODSTOP ACTIEF — reden: {reason}")

        if self._stop_callback:
            try:
                self._stop_callback(reason)
            except Exception:
                pass

        if not already_stopped:
            # Keep the red state visible for a moment before closing.
            self.root.after(50, self._close_after_stop)

    def _close_after_stop(self):
        # Menno v1 closes only Menno itself.
        # Later versions can add tracked child-process cleanup.
        self.root.destroy()

    def request_normal_shutdown(self):
        """Normal user-requested shutdown."""
        with self._lock:
            self._armed = False
            self._stopped = True

        if self._global_listener is not None:
            try:
                self._global_listener.stop()
            except Exception:
                pass

        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def _set_status(self, message: str):
        if self._status_callback:
            try:
                self._status_callback(message)
            except Exception:
                pass
