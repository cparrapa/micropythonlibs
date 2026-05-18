import time
import board
from screen import Screen
from math import sin, cos, pi

__version__ = "1.0.6"


class Turtle:

  def __init__(self):
    if not Screen.instance:
      self.screen = Screen()
    else:
      self.screen = Screen.instance
    self._position = (0.0, 0.0)
    self._x = 80
    self._y = 64
    self._angle = 0
    self._old_heading = 0
    self._fillcolor = (255,0,0)
    self._fillpath = None
    self._fullcircle = 360.0
    self._drawing = True
    self.degree_to_radians = pi / 180
    self.init()

  def init(self):
    board.DISPLAY.rotation = 90
    if Screen.mode == 'turtle':
      return
    board.DISPLAY.show(Screen.group)
    board.DISPLAY.refresh()
    board.DISPLAY.auto_refresh = True
    self.screen.clear()
    Screen.mode = 'turtle'
  
  def _goto(self, x, y):
    if self._drawing:
      self.screen.line(round(self._x), round(self._y), round(x), round(y), self._fillcolor)
    if self._fillpath is not None:
      self._fillpath.append((x, y))
    self._position = (x, y)
    self._x = x
    self._y = y

  def goto(self, x, y):
    self._distance = abs(self._x - x) + abs(self._y - y)
    self._goto(x, y)
    time.sleep(0.005)


  def forward(self, distance):
    x1 = distance * cos(self._angle * self.degree_to_radians)
    y1 = distance * sin(self._angle * self.degree_to_radians)
    self._distance = distance
    self._goto(self._x + x1, self._y + y1)
    time.sleep(0.005)

  def right(self, angle):
    self._angle += angle

  def left(self, angle):
    self._angle -= angle

  def setx(self, x):
    self._distance = abs(x - self._x)
    self._goto(x, self._y)
    time.sleep(0.005)

  def sety(self, y):
    self._distance = abs(y - self._y)
    self._goto(self._x, y)
    time.sleep(0.005)

  def clear(self):
    self.screen.fill(0)
    time.sleep(0.005)
  
  def _rotate(self, angle):
    self._angle -= angle

  def setheading(self, to_angle):
    self._angle = -to_angle

  def circle(self, radius, extent=None):
    if extent is None:
      extent = self._fullcircle
    time.sleep(0.005)
    
    frac = abs(extent)/self._fullcircle
    steps = 1+int(min(11+abs(radius)/6.0, 59.0)*frac)
    w = 1.0 * extent / steps
    w2 = 0.5 * w
    l = 2.0 * radius * sin(w2 * pi / 180.0)
    if radius < 0:
      l, w, w2 = -l, -w, -w2
    self._rotate(w2)
    for i in range(steps):
      self.forward(l)
      self._rotate(w)
    self._rotate(-w2)

  def pendown(self):
    self._drawing = True

  def penup(self):
    self._drawing = False

  def dot(self, size=5):
    self.screen.circle(round(self._x), round(self._y), round(size), self._fillcolor, 1)

  def fillcolor(self, color):
    self._fillcolor = color

  def begin_fill(self):
    self._fillpath = [(self._x, self._y)]

  def end_fill(self):
    if self._fillpath != None and len(self._fillpath) > 2:
      x0, y0 = self._fillpath[0]#50,100
      num = len(self._fillpath)
      for i in range(1, num):
        if i+1 < num:
          self.screen.triangle(round(x0), round(y0), round(self._fillpath[i][0]), round(self._fillpath[i][1]), round(self._fillpath[i+1][0]), round(self._fillpath[i+1][1]), self._fillcolor, 1)
    else:
      print("No path to fill.")
    self._fillpath = None


if __name__ == '__main__':
    t = Turtle()
    t.forward(10)
    t.left(90)
    t.forward(10)
    time.sleep(3)

