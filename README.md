# One Inch Gym Timer

A desktop gym timer built with Python and Tkinter. It has a six-digit amber
seven-segment display with two blinking colon delimiters.

## Run

```powershell
py timer.py
```

Python must be installed with Tk support (included with most standard Windows
Python installers).

Both apps display the University of Gibraltar logo from `logo.png` alongside
their app title. Keep the logo in the same folder as the Python scripts.

## Four-bit seven-segment decoder

Run the standalone binary-input display app:

```powershell
py binary_seven_segment.py
```

Enter four binary digits to drive one seven-segment digit. Inputs `0000` to
`1001` display decimal digits 0–9; `1010` to `1111` display hexadecimal
`A`, `b`, `C`, `d`, `E`, and `F`. Click the four switches (ordered 8, 4, 2, 1)
to set or clear individual bits; the switches and text input stay synchronized.

## Controls

- **Operation** switches between stopwatch and countdown modes.
- **Reset** returns the stopwatch to zero or restores the countdown preset.
- **Clock** toggles the display between the timer and local 24-hour time.
- **Set** selects minutes, seconds, then hundredths for adjustment; press it
  again to finish.
- **Up / Down** adjust the selected value. If no field is selected, they adjust
  seconds.
- **Start** starts or pauses the timer. A countdown reaching zero stops.
- **Off / On** switches the display off and back on; switching off pauses a
  running timer.

Keyboard shortcuts: Space (start/stop), R (reset), O (operation), C (clock),
S (set), and Up/Down arrows (adjust).
