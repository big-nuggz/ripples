from os import get_terminal_size
from sys import stdout
import re

import numpy as np

from ripples.renderer.renderer import Renderer
from ripples.ripples import Ripples


class ConsoleRenderer(Renderer):
  def __init__(self, ripples: Ripples, offset=0):
    """
    renderer for terminal, requires colorama for ANSI escapes

    Args:
        ripples (Ripples): Ripples object
        offset (int, optional): Y-offset of the output. Defaults to 0.
    """
    super().__init__(ripples)
    self.terminal_width, _ = get_terminal_size()
    self.offset = offset

  def clear(self):
    stdout.write('\033[H')

    if self.offset > 0:
      stdout.write(f'\033[{self.offset}B')

    stdout.flush()

  def render(self):
    position = self.ripples.get_positions()

    for y in range(self.ripples.height):
      # clip to +- 1 and map to block characters for shading
      row = position[y, :]
      row[row > 1] = 1
      row[row < -1] = -1
      row = str((((row + 1) / 2) * 4).astype(np.int8))
      row = re.sub(r'[\s\[\]]', '', row)

      for n, c in zip(range(5), [' ', '░', '▒', '▓', '█']):
        row = row.replace(f'{n}', c * 2)

      stdout.write(row + ' ' * (self.terminal_width - len(row)))
      stdout.flush()