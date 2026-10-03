from ripples.ripples import Ripples


class Renderer:
  # renderer base class
  def __init__(self, ripples: Ripples):
    self.ripples = ripples

  def clear(self):
    pass

  def render(self):
    pass