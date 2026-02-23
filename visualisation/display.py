"""
Display module: Provides terminal rendering and animation capabilities.
Classes: DynamicTerminal
"""

import sys
import os


if os.name == 'nt':
    os.system('color')


class DynamicTerminal:
    """Provides dynamic terminal rendering for simulation animation."""

    def __init__(self, nrows=12):
        """Initialize terminal by printing empty lines."""
        for i in range(0, nrows):
            print("")

    def move_cursor_up(self, lines):
        """Move cursor up <lines> lines."""
        sys.stdout.write(f'\x1b[{lines}A')   # ESC[<n>A
        sys.stdout.flush()

    def rewrite_lines(self, new_lines):
        """Write <new_lines> starting at the current cursor position."""
        sys.stdout.write('\n'.join(new_lines) + '\n')
        sys.stdout.flush()

    def clear_line(self):
        """Clear the entire current line (ESC[2K)."""
        sys.stdout.write('\x1b[2K')
        sys.stdout.flush()

    def render(self, text, nrows):
        """Render text by moving cursor up and rewriting lines."""
        self.move_cursor_up(nrows)
        self.clear_line()
        self.rewrite_lines(text)
