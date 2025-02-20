import time
from blessed import Terminal

term = Terminal()

def display_animation():
    """Display a cool animation."""
    frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    for frame in frames:
        print(term.move_xy(0, term.height - 1) + term.bold(frame), end="", flush=True)
        time.sleep(0.1)
