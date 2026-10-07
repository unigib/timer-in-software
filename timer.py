"""A small Tkinter gym timer with a six-digit seven-segment display."""

from pathlib import Path
import time
import tkinter as tk
from tkinter import ttk


class SevenSegmentDisplay(tk.Canvas):
    """Canvas-based six-digit display with two colon separators."""

    GREEN = "#00ff00"
    GREEN_DIM = "#003b00"
    RED = "#ff2020"
    RED_DIM = "#3b0808"

    DIGITS = {
        "0": "abcdef",
        "1": "bc",
        "2": "abged",
        "3": "abgcd",
        "4": "fgbc",
        "5": "afgcd",
        "6": "afgecd",
        "7": "abc",
        "8": "abcdefg",
        "9": "abfgcd",
    }

    def __init__(self, master):
        super().__init__(
            master,
            height=200,
            background="#101713",
            highlightthickness=0,
        )
        self.value = "000000"
        self.blink_colons = True
        self.dim_field = None
        self.bind("<Configure>", self._draw)

    def show(self, value, blink_colons=True, dim_field=None):
        self.value = value
        self.blink_colons = blink_colons
        self.dim_field = dim_field
        self._draw()

    def _draw(self, _event=None):
        self.delete("all")
        width = max(self.winfo_width(), 1)
        height = max(self.winfo_height(), 1)
        digit_height = min((height - 24) / 1.5, (width - 36) / 4.9)
        digit_height = max(digit_height, 20)
        digit_width = digit_height * 0.58
        gap = digit_height * 0.08
        colon_width = digit_height * 0.22
        total_width = 6 * digit_width + 2 * colon_width + 7 * gap
        x = (width - total_width) / 2
        y = (height - digit_height) / 2

        for index, character in enumerate(self.value):
            if index in (2, 4):
                self._draw_colon(x, y, digit_height)
                x += colon_width + gap
            dim = self.dim_field == index // 2
            color = self.GREEN if index < 2 else self.RED
            dim_color = self.GREEN_DIM if index < 2 else self.RED_DIM
            self._draw_digit(
                x, y, digit_width, digit_height, character, dim, color, dim_color
            )
            x += digit_width + gap

    def _draw_colon(self, x, y, digit_height):
        if not self.blink_colons:
            return
        radius = digit_height * 0.045
        center_x = x + digit_height * 0.11
        for center_y in (y + digit_height * 0.36, y + digit_height * 0.68):
            self.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                fill="#ffb43b",
                outline="",
            )

    def _draw_digit(self, x, y, width, height, character, dim, color, dim_color):
        thickness = min(width * 0.18, height * 0.08)
        middle = height / 2
        t = thickness
        segments = {
            "a": [(x + t, y), (x + width - t, y), (x + width - 2 * t, y + t), (x + 2 * t, y + t)],
            "g": [
                (x + 2 * t, y + middle - t / 2),
                (x + t, y + middle),
                (x + 2 * t, y + middle + t / 2),
                (x + width - 2 * t, y + middle + t / 2),
                (x + width - t, y + middle),
                (x + width - 2 * t, y + middle - t / 2),
            ],
            "d": [
                (x + 2 * t, y + height - t),
                (x + width - 2 * t, y + height - t),
                (x + width - t, y + height),
                (x + t, y + height),
            ],
            "f": [(x, y + t), (x + t, y + 2 * t), (x + t, y + middle - t), (x, y + middle - 2 * t)],
            "b": [
                (x + width, y + t),
                (x + width, y + middle - 2 * t),
                (x + width - t, y + middle - t),
                (x + width - t, y + 2 * t),
            ],
            "e": [
                (x, y + middle + 2 * t),
                (x + t, y + middle + t),
                (x + t, y + height - 2 * t),
                (x, y + height - t),
            ],
            "c": [
                (x + width, y + middle + 2 * t),
                (x + width, y + height - t),
                (x + width - t, y + height - 2 * t),
                (x + width - t, y + middle + t),
            ],
        }
        lit = set() if dim else set(self.DIGITS.get(character, ""))
        for name, points in segments.items():
            coordinates = [coordinate for point in points for coordinate in point]
            self.create_polygon(
                coordinates,
                fill=color if name in lit else dim_color,
                outline="",
            )


class GymTimer:
    MAX_TIME = 99 * 60 * 100 + 59 * 100 + 99
    TICK_MS = 30

    def __init__(self, root):
        self.root = root
        self.root.title("One Inch Gym Timer")
        self.root.configure(background="#17201b")
        self.root.geometry("900x520")
        self.root.minsize(660, 440)

        self.mode = "STOPWATCH"
        self.clock_mode = False
        self.powered_on = True
        self.running = False
        self.timer_value = 0
        self.countdown_preset = 60 * 100
        self.edit_field = None
        self.run_started_at = 0.0
        self.run_start_value = 0
        self._after_id = None

        style = ttk.Style()
        style.configure(
            "Timer.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(10, 11),
            foreground="#17201b",
            background="#d9e5dc",
        )
        style.map(
            "Timer.TButton",
            background=[("active", "#ffb43b"), ("disabled", "#66716a")],
        )

        content = tk.Frame(root, background="#17201b", padx=28, pady=22)
        content.pack(fill="both", expand=True)

        self.logo_image = tk.PhotoImage(
            file=str(Path(__file__).with_name("logo.png"))
        ).subsample(3, 3)
        brand_header = tk.Frame(content, background="#17201b")
        brand_header.pack(anchor="w")
        tk.Label(
            brand_header,
            image=self.logo_image,
            background="#17201b",
        ).pack(side="left", padx=(0, 14))
        tk.Label(
            brand_header,
            text="ONE INCH  /  GYM TIMER",
            font=("Segoe UI", 15, "bold"),
            foreground="#d9e5dc",
            background="#17201b",
        ).pack(side="left")

        self.status = tk.StringVar()
        self.status_label = tk.Label(
            content,
            textvariable=self.status,
            font=("Segoe UI", 10, "bold"),
            foreground="#8ea394",
            background="#17201b",
            pady=12,
        )
        self.status_label.pack(anchor="w")

        self.display = SevenSegmentDisplay(content)
        self.display.pack(fill="x", expand=True, pady=(0, 14))

        controls = tk.Frame(content, background="#17201b")
        controls.pack(fill="x")
        buttons = [
            ("OPERATION", self.operation),
            ("RESET", self.reset),
            ("CLOCK", self.toggle_clock),
            ("SET", self.set_button),
            ("OFF / ON", self.toggle_power),
            ("START", self.start_stop),
            ("UP", lambda: self.adjust(1)),
            ("DOWN", lambda: self.adjust(-1)),
        ]
        for index, (label, command) in enumerate(buttons):
            button = ttk.Button(
                controls,
                text=label,
                command=command,
                style="Timer.TButton",
            )
            button.grid(row=index // 4, column=index % 4, sticky="ew", padx=4, pady=4)
            if label != "OFF / ON":
                button.bind("<Button-1>", self._ignore_when_powered_off)
            controls.columnconfigure(index % 4, weight=1)
        self.control_buttons = [
            child for child in controls.winfo_children() if isinstance(child, ttk.Button)
        ]

        tk.Label(
            content,
            text="SPACE  start/stop     R  reset     O  operation     C  clock     S  set     ↑ / ↓  adjust",
            font=("Segoe UI", 9),
            foreground="#8ea394",
            background="#17201b",
            pady=12,
        ).pack(anchor="w")

        root.bind("<space>", lambda _event: self.start_stop())
        root.bind("<KeyPress-r>", lambda _event: self.reset())
        root.bind("<KeyPress-o>", lambda _event: self.operation())
        root.bind("<KeyPress-c>", lambda _event: self.toggle_clock())
        root.bind("<KeyPress-s>", lambda _event: self.set_button())
        root.bind("<Up>", lambda _event: self.adjust(1))
        root.bind("<Down>", lambda _event: self.adjust(-1))
        root.protocol("WM_DELETE_WINDOW", self.close)
        self._refresh()
        self._schedule_tick()

    def _ignore_when_powered_off(self, _event):
        if not self.powered_on:
            return "break"
        return None

    def _current_value(self):
        if not self.running:
            return self.timer_value
        elapsed = int((time.monotonic() - self.run_started_at) * 100)
        if self.mode == "STOPWATCH":
            return min(self.run_start_value + elapsed, self.MAX_TIME)
        return max(self.run_start_value - elapsed, 0)

    def _schedule_tick(self):
        self._after_id = self.root.after(self.TICK_MS, self._tick)

    def _tick(self):
        self._after_id = None
        if self.running:
            value = self._current_value()
            if self.mode == "STOPWATCH" and value >= self.MAX_TIME:
                self.timer_value = self.MAX_TIME
                self.running = False
            elif self.mode == "COUNTDOWN" and value <= 0:
                self.timer_value = 0
                self.running = False
            else:
                self.timer_value = value
        self._refresh()
        self._schedule_tick()

    def _refresh(self):
        if self.clock_mode:
            clock = time.localtime()
            digits = time.strftime("%H%M%S", clock)
            blink = clock.tm_sec % 2 == 0
            details = "LOCAL CLOCK  •  CLOCK TO RETURN"
        else:
            value = self._current_value()
            minutes, remainder = divmod(value, 60 * 100)
            seconds, centiseconds = divmod(remainder, 100)
            digits = f"{minutes:02d}{seconds:02d}{centiseconds:02d}"
            blink = int(time.monotonic() * 2) % 2 == 0
            details = self.mode
            if self.running:
                details += "  •  RUNNING"
            elif self.edit_field is not None:
                details += f"  •  SET {('MINUTES', 'SECONDS', 'HUNDREDTHS')[self.edit_field]}"
            else:
                details += "  •  READY"
        if not self.powered_on:
            digits = "      "
            details = "POWER OFF  •  PRESS OFF / ON"
        self.display.show(
            digits,
            blink_colons=blink,
            dim_field=self.edit_field if self.edit_field is not None and blink else None,
        )
        self.status.set(details)
        self.status_label.configure(
            foreground="#ffb43b" if self.running else "#8ea394"
        )

    def operation(self):
        if not self.powered_on or self.clock_mode:
            return
        self.running = False
        self.edit_field = None
        self.mode = "COUNTDOWN" if self.mode == "STOPWATCH" else "STOPWATCH"
        self.timer_value = self.countdown_preset if self.mode == "COUNTDOWN" else 0
        self._refresh()

    def reset(self):
        if not self.powered_on or self.clock_mode:
            return
        self.running = False
        self.edit_field = None
        self.timer_value = (
            self.countdown_preset if self.mode == "COUNTDOWN" else 0
        )
        self._refresh()

    def toggle_clock(self):
        if not self.powered_on:
            return
        self.clock_mode = not self.clock_mode
        self.edit_field = None
        self._refresh()

    def set_button(self):
        if not self.powered_on or self.clock_mode or self.running:
            return
        if self.edit_field is None:
            self.edit_field = 0
        elif self.edit_field < 2:
            self.edit_field += 1
        else:
            self.edit_field = None
        self._refresh()

    def adjust(self, direction):
        if not self.powered_on or self.clock_mode or self.running:
            return
        field = self.edit_field
        if field is None:
            field = 1
        steps = (60 * 100, 100, 1)
        self.timer_value = max(
            0, min(self.MAX_TIME, self.timer_value + direction * steps[field])
        )
        if self.mode == "COUNTDOWN":
            self.countdown_preset = self.timer_value
        self._refresh()

    def start_stop(self):
        if not self.powered_on or self.clock_mode:
            return
        if self.running:
            self.timer_value = self._current_value()
            self.running = False
        else:
            if self.mode == "COUNTDOWN" and self.timer_value == 0:
                self.timer_value = self.countdown_preset
            if self.timer_value >= self.MAX_TIME and self.mode == "STOPWATCH":
                self.timer_value = 0
            self.run_start_value = self.timer_value
            self.run_started_at = time.monotonic()
            self.running = True
            self.edit_field = None
        self._refresh()

    def toggle_power(self):
        self.powered_on = not self.powered_on
        if not self.powered_on:
            if self.running:
                self.timer_value = self._current_value()
            self.running = False
            self.edit_field = None
        self._refresh()

    def close(self):
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
        self.root.destroy()


def main():
    root = tk.Tk()
    GymTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
