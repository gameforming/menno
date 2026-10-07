import time

from screen import get_cursor_position


def get_position() -> tuple[int, int]:
    """Read the cursor position without moving it."""
    return get_cursor_position()


def move_to(x: int, y: int, duration: float = 0.15, safety=None) -> bool:
    """
    Move the cursor using pyautogui.
    Safety must be checked before and during the movement.
    """
    if safety is not None and safety.is_stopped():
        return False

    try:
        import pyautogui
    except ImportError:
        raise RuntimeError("pyautogui ontbreekt. Installeer requirements.txt.")

    pyautogui.moveTo(int(x), int(y), duration=max(0.0, float(duration)))

    if safety is not None and safety.is_stopped():
        return False

    return True


def click(x: int | None = None, y: int | None = None, safety=None) -> bool:
    """Click at x/y, or at the current cursor location."""
    if safety is not None and safety.is_stopped():
        return False

    try:
        import pyautogui
    except ImportError:
        raise RuntimeError("pyautogui ontbreekt. Installeer requirements.txt.")

    if x is not None and y is not None:
        pyautogui.click(int(x), int(y))
    else:
        pyautogui.click()

    return safety is None or not safety.is_stopped()


def type_text(text: str, interval: float = 0.01, safety=None) -> bool:
    """Type text with pyautogui."""
    if safety is not None and safety.is_stopped():
        return False

    try:
        import pyautogui
    except ImportError:
        raise RuntimeError("pyautogui ontbreekt. Installeer requirements.txt.")

    pyautogui.write(str(text), interval=max(0.0, float(interval)))
    return safety is None or not safety.is_stopped()


def press(key: str, safety=None) -> bool:
    """Press a single keyboard key."""
    if safety is not None and safety.is_stopped():
        return False

    try:
        import pyautogui
    except ImportError:
        raise RuntimeError("pyautogui ontbreekt. Installeer requirements.txt.")

    pyautogui.press(key)
    return safety is None or not safety.is_stopped()


def emergency_test_note() -> str:
    return (
        "De safety layer heeft voorrang op normale cursoracties. "
        "De huidige v1 voert alleen cursoracties uit als deze expliciet "
        "door een lokaal Python-script worden aangeroepen."
    )
