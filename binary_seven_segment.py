"""Interactive four-bit binary-to-seven-segment decoder."""

from pathlib import Path
import tkinter as tk


SEGMENTS_BY_HEX_DIGIT = {
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
    "A": "abcefg",
    "b": "cdefg",
    "C": "adef",
    "d": "bcdeg",
    "E": "adefg",
    "F": "aefg",
}


def decode_binary(bits):
    """Return the hexadecimal seven-segment symbol for a four-bit input."""
    if len(bits) != 4 or any(bit not in "01" for bit in bits):
        raise ValueError("Input must contain exactly four binary digits.")
    value = int(bits, 2)
    return "0123456789AbCdEF"[value]


class SevenSegmentDigit(tk.Canvas):
    """Draw one seven-segment digit on a resizable Tkinter canvas."""

    ON_COLOR = "#39ff14"
    OFF_COLOR = "#173018"
    BACKGROUND = "#0b100c"

    def __init__(self, master):
        super().__init__(
            master,
            background=self.BACKGROUND,
            highlightthickness=0,
            width=300,
            height=360,
        )
        self.symbol = "0"
        self.bind("<Configure>", self._draw)

    def show(self, symbol):
        self.symbol = symbol
        self._draw()

    def _draw(self, _event=None):
        self.delete("all")
        width = max(self.winfo_width(), 1)
        height = max(self.winfo_height(), 1)
        digit_height = min(height * 0.82, width * 1.45)
        digit_width = digit_height * 0.58
        x = (width - digit_width) / 2
        y = (height - digit_height) / 2
        thickness = digit_height * 0.085
        middle = y + digit_height / 2
        t = thickness
        w = digit_width
        h = digit_height

        polygons = {
            "a": [(x + t, y), (x + w - t, y), (x + w - 2 * t, y + t), (x + 2 * t, y + t)],
            "g": [
                (x + 2 * t, middle - t / 2),
                (x + t, middle),
                (x + 2 * t, middle + t / 2),
                (x + w - 2 * t, middle + t / 2),
                (x + w - t, middle),
                (x + w - 2 * t, middle - t / 2),
            ],
            "d": [
                (x + 2 * t, y + h - t),
                (x + w - 2 * t, y + h - t),
                (x + w - t, y + h),
                (x + t, y + h),
            ],
            "f": [(x, y + t), (x + t, y + 2 * t), (x + t, middle - t), (x, middle - 2 * t)],
            "b": [
                (x + w, y + t),
                (x + w, middle - 2 * t),
                (x + w - t, middle - t),
                (x + w - t, y + 2 * t),
            ],
            "e": [
                (x, middle + 2 * t),
                (x + t, middle + t),
                (x + t, y + h - 2 * t),
                (x, y + h - t),
            ],
            "c": [
                (x + w, middle + 2 * t),
                (x + w, y + h - t),
                (x + w - t, y + h - 2 * t),
                (x + w - t, middle + t),
            ],
        }
        lit_segments = set(SEGMENTS_BY_HEX_DIGIT[self.symbol])
        for name, points in polygons.items():
            coordinates = [coordinate for point in points for coordinate in point]
            self.create_polygon(
                coordinates,
                fill=self.ON_COLOR if name in lit_segments else self.OFF_COLOR,
                outline="",
            )


class BinarySwitch(tk.Canvas):
    """Clickable, drawn toggle switch for one binary input bit."""

    def __init__(self, master, weight, on_change):
        super().__init__(
            master,
            width=72,
            height=94,
            background="#17201b",
            highlightthickness=0,
            cursor="hand2",
        )
        self.weight = weight
        self.on_change = on_change
        self.value = 0
        self.bind("<Button-1>", self._toggle)
        self.bind("<Configure>", self._draw)
        self._draw()

    def set_value(self, value):
        self.value = int(value)
        self._draw()

    def _toggle(self, _event=None):
        self.value = 1 - self.value
        self._draw()
        self.on_change()

    def _draw(self, _event=None):
        self.delete("all")
        width = max(self.winfo_width(), 1)
        center = width / 2
        self.create_text(
            center,
            12,
            text=str(self.weight),
            fill="#9daf9f",
            font=("Segoe UI", 9, "bold"),
        )
        self.create_text(
            center,
            31,
            text=str(self.value),
            fill="#39ff14" if self.value else "#bac4bb",
            font=("Consolas", 14, "bold"),
        )
        track_top, track_bottom = 48, 84
        self.create_rectangle(
            center - 13,
            track_top,
            center + 13,
            track_bottom,
            fill="#174d19" if self.value else "#344038",
            outline="",
        )
        knob_y = track_top + 10 if self.value else track_bottom - 10
        self.create_oval(
            center - 9,
            knob_y - 9,
            center + 9,
            knob_y + 9,
            fill="#39ff14" if self.value else "#b1bcb3",
            outline="",
        )


class BinaryDecoderApp:
    def __init__(self, root):
        self.root = root
        root.title("Four-Bit Seven-Segment Decoder")
        root.geometry("460x590")
        root.minsize(380, 500)
        root.configure(background="#17201b")

        panel = tk.Frame(root, background="#17201b", padx=28, pady=22)
        panel.pack(fill="both", expand=True)

        self.logo_image = tk.PhotoImage(
            file=str(Path(__file__).with_name("logo.png"))
        ).subsample(3, 3)
        brand_header = tk.Frame(panel, background="#17201b")
        brand_header.pack(anchor="w")
        tk.Label(
            brand_header,
            image=self.logo_image,
            background="#17201b",
        ).pack(side="left", padx=(0, 14))
        title_block = tk.Frame(brand_header, background="#17201b")
        title_block.pack(side="left")
        tk.Label(
            title_block,
            text="BINARY → SEVEN-SEGMENT",
            font=("Segoe UI", 15, "bold"),
            foreground="#e4eee6",
            background="#17201b",
        ).pack(anchor="w")
        tk.Label(
            title_block,
            text="Enter a 4-bit value (0000–1111)",
            font=("Segoe UI", 10),
            foreground="#9daf9f",
            background="#17201b",
        ).pack(anchor="w")

        self.bits = tk.StringVar(value="0000")
        validate_command = (root.register(self._valid_bits), "%P")
        self.input = tk.Entry(
            panel,
            textvariable=self.bits,
            validate="key",
            validatecommand=validate_command,
            font=("Consolas", 24, "bold"),
            justify="center",
            width=6,
            background="#0b100c",
            foreground="#39ff14",
            insertbackground="#39ff14",
            relief="flat",
        )
        self.input.pack(anchor="w", ipady=7)
        self.input.bind("<KeyRelease>", self._update)

        tk.Label(
            panel,
            text="INPUT SWITCHES  (MSB → LSB)",
            font=("Segoe UI", 9, "bold"),
            foreground="#9daf9f",
            background="#17201b",
            pady=16,
        ).pack(anchor="w")
        switch_row = tk.Frame(panel, background="#17201b")
        switch_row.pack(anchor="w")
        self.switches = []
        for weight in (8, 4, 2, 1):
            switch = BinarySwitch(switch_row, weight, self._switch_changed)
            switch.pack(side="left", padx=(0, 10))
            self.switches.append(switch)

        self.value_label = tk.StringVar()
        tk.Label(
            panel,
            textvariable=self.value_label,
            font=("Segoe UI", 10),
            foreground="#9daf9f",
            background="#17201b",
            pady=10,
        ).pack(anchor="w")

        self.display = SevenSegmentDigit(panel)
        self.display.pack(fill="both", expand=True, pady=(4, 0))
        self._update()

    def _switch_changed(self):
        value = sum(switch.weight * switch.value for switch in self.switches)
        bits = format(value, "04b")
        self.bits.set(bits)
        self._update()

    @staticmethod
    def _valid_bits(proposed):
        return len(proposed) <= 4 and all(bit in "01" for bit in proposed)

    def _update(self, _event=None):
        bits = self.bits.get()
        if len(bits) != 4:
            self.value_label.set("Type four bits to decode.")
            return
        for switch, bit in zip(self.switches, bits):
            switch.set_value(bit)
        symbol = decode_binary(bits)
        value = int(bits, 2)
        self.display.show(symbol)
        self.value_label.set(f"{bits}  =  {value} decimal  =  {symbol} hexadecimal")


def main():
    root = tk.Tk()
    BinaryDecoderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
