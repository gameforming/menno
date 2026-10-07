import ctypes
import tkinter as tk


def get_screen_size() -> tuple[int, int]:
    """
    Return the primary screen size in pixels.
    Uses tkinter first and falls back to Windows APIs.
    """
    try:
        root = tk._default_root
        if root is not None:
            return root.winfo_screenwidth(), root.winfo_screenheight()
    except Exception:
        pass

    try:
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except Exception:
        return 0, 0


def get_cursor_position() -> tuple[int, int]:
    """Return the current global Windows cursor position."""
    try:
        point = ctypes.wintypes.POINT()
    except AttributeError:
        from ctypes import wintypes
        point = wintypes.POINT()

    try:
        ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
        return int(point.x), int(point.y)
    except Exception:
        return 0, 0
