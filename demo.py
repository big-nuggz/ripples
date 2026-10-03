from os import get_terminal_size
from sys import exit, stdout
import time
from datetime import datetime

import numpy as np
import colorama

from ripples.ripples import Ripples
from ripples.renderer.console_renderer import ConsoleRenderer


# -------- params
target_fps = 30
ripple_chance = 30 # percent every frame
grid_size = (30, 20)
# -------- end of params

colorama.init() # must be called ONLY ONCE

rng = np.random.default_rng()

target_delta_s = 1 / target_fps

ripples = Ripples(grid_size[0], grid_size[1])
renderer = ConsoleRenderer(ripples, offset=1)

help_text = 'try squinting! Ctrl + C to exit'
stdout.write(f'\033[H{help_text}{" " * (get_terminal_size()[0] - len(help_text))}')
stdout.flush()

try:
  while True:
    time_start = datetime.now()

    # render last frame
    renderer.clear()
    renderer.render()

    # pull random point
    if rng.integers(0, 100) < ripple_chance:
      ripples.add_random(rng.integers(1, 10))

    # physics step
    ripples.step()

    # wait
    delta = (datetime.now() - time_start).total_seconds()
    time.sleep(max(target_delta_s - delta, 0.001)) # wait at least a ms if delta exceeds target

except KeyboardInterrupt as e:
  exit()

finally:
  colorama.deinit()
  print(':D')
