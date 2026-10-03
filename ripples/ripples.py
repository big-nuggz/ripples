import numpy as np


class Ripples:
  def __init__(self, width: int, height: int, propagation=0.5, dampening=0.1):
    """
    2D wave simulator

    Args:
        width (int): simulation grid width
        height (int): simulation grid height
        propagation (float, optional): physics constant, too high value will break the simulation. Defaults to 0.5.
        dampening (float, optional): friction factor to eventually slow the waves down to halt. Defaults to 0.05.
    """
    self.height = height
    self.width = width
    self.dampening = dampening
    self.propagation = propagation

    self.position = np.zeros((height + 2, width + 2))
    self.velocity = np.zeros((height + 2, width + 2))

    self.rng = np.random.default_rng()

  def clear(self):
    self.position *= 0
    self.velocity *= 0

  def step(self):
    """
    calculates velocity of every point on the grid for the next step, then applies to the positions
    """
    acc = np.zeros_like(self.velocity)

    acc += np.roll(self.position, 1, 0)
    acc += np.roll(self.position, -1, 0)
    acc += np.roll(self.position, 1, 1)
    acc += np.roll(self.position, -1, 1)
    acc -= self.position * 4

    self.velocity += self.propagation ** 2 * acc - self.dampening * self.velocity

    # pin edges
    self.velocity[0, :] = 0.0
    self.velocity[-1, :] = 0.0
    self.velocity[:, 0] = 0.0
    self.velocity[:, -1] = 0.0

    self.position[0, :] = 0.0
    self.position[-1, :] = 0.0
    self.position[:, 0] = 0.0
    self.position[:, -1] = 0.0

    self.position += self.velocity

  def add_random(self, velocity: float):
    """
    randomly select a point on the grid and adds given velocity

    Args:
        velocity (float): velocity
    """
    x = self.rng.integers(1, self.width)
    y = self.rng.integers(1, self.height)

    self.velocity[y, x] += velocity

  def get_positions(self):
    return self.position[1:-1, 1:-1].copy()
