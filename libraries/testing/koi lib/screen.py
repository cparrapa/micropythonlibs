import board
import espidf
from displayio import Group,Bitmap,ColorConverter,Colorspace,TileGrid,Palette
import bitmaptools
from math import sin,cos,pi

__version__ = "1.0.12"

colorMap={'white':(255,255,255), 'black':(0,0,0), 'red':(255,0,0), 'orange':(255,165,0), 'yellow':(255,255,0),
'green':(0,255,0), 'blue':(0,0,255), 'cyan':(0,127,255), 'purple':(148,0,211), 'pink':(255,105,180) }

def getColHex(t):
  if type(t) == str:
    if len(t) == 7 and t[0] == '#':
      t = (int(t[1:3], 16), int(t[3:5], 16),int(t[5:8], 16))
    else:
      t = colorMap[t]
  if type(t) == int:
    color = ((t & 0b11111000) << 8) | ((t & 0b11111100) << 3) | (t >> 3)
  elif type(t) == tuple:
    if len(t) == 3:
      color = ((t[0] & 0b11111000) << 8) | ((t[1] & 0b11111100) << 3) | (t[2] >> 3)
    elif len(t) == 1:
      t = t[0]&0xff
      color = ((t & 0b11111000) << 8) | ((t & 0b11111100) << 3) | (t >> 3)
  else:
    color = 0
  return color

class Screen:
  mode = None
  group = None
  instance = None
  def __init__(self):
    if not Screen.instance:
      self.group = Group()
      self.bitmap = Bitmap(160,160,0xffff)
      self.converter = ColorConverter(input_colorspace=Colorspace.RGB565)
      self.tile = TileGrid(self.bitmap,x=0,y=0,pixel_shader=self.converter)
      self.group.append(self.tile)
      Screen.group = self.group
      Screen.instance = self
    else:
      self.bitmap = Screen.instance.bitmap
    self.init()

  def init(self):
    if Screen.mode == 'screen':
      return
    board.DISPLAY.show(Screen.group)
    board.DISPLAY.refresh()
    board.DISPLAY.auto_refresh = True
    Screen.mode = 'screen'

  def setBrightness(self,state):
    if state:
      board.DISPLAY.brightness = 1
    else:
      board.DISPLAY.brightness = 0
  
  def setRotation(self,dir):
    board.DISPLAY.rotation = dir

  def autoRefresh(self,switch):
    board.DISPLAY.auto_refresh = switch
  
  def refresh(self):
    board.DISPLAY.refresh()

  def fill(self, color=255):
    color = getColHex(color)
    self.bitmap.fill(color)

  def clear(self):
    self.fill(0)

  def pixel(self,x,y,color=255):
    color = getColHex(color)
    self.bitmap[160*y+x] = color

  def _draw_filled(self,x0,y0,x1,y1,x2,y2,col):
      if y0 == y2:  # Handle awkward all-on-same-line case as its own thing
        a = x0
        b = x0
        if x1 < a:
          a = x1
        elif x1 > b:
          b = x1

        if x2 < a:
          a = x2
        elif x2 > b:
          b = x2
        self._line(a, y0, b, y0, col)
        return

      if y1 == y2:
        last = y1  # Include y1 scanline
      else:
        last = y1 - 1  # Skip it

      # Upper Triangle
      for y in range(y0, last + 1):
        a = round(x0 + (x1 - x0) * (y - y0) / (y1 - y0))
        b = round(x0 + (x2 - x0) * (y - y0) / (y2 - y0))
        if a > b:
          a, b = b, a
        self._line(a, y, b, y, col)
      # Lower Triangle
      for y in range(last + 1, y2 + 1):
        a = round(x1 + (x2 - x1) * (y - y1) / (y2 - y1))
        b = round(x0 + (x2 - x0) * (y - y0) / (y2 - y0))

        if a > b:
          a, b = b, a
        self._line(a, y, b, y, col)

  def _line(self,x0,y0,x1,y1,color):
    if x0 == x1:
      if y0 > y1:
        y0, y1 = y1, y0
      for _h in range(y0, y1 + 1):
        try:
          self.bitmap[x0, _h] = color
        except IndexError:
          pass
    elif y0 == y1:
      if x0 > x1:
        x0, x1 = x1, x0
      for _w in range(x0, x1 + 1):
        try: 
          self.bitmap[_w, y0] = color
        except IndexError:
          pass
    else:
      steep = abs(y1 - y0) > abs(x1 - x0)
      if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

      if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

      dx = x1 - x0
      dy = abs(y1 - y0)

      err = dx / 2

      if y0 < y1:
        ystep = 1
      else:
        ystep = -1

      for x in range(x0, x1 + 1):
        try:
          if steep:
            self.bitmap[y0, x] = color
          else:
            self.bitmap[x, y0] = color
        except IndexError:
          pass
        err -= dy
        if err < 0:
          y0 += ystep
          err += dx
    

  def line(self,x0,y0,x1,y1,color=255):
    color = getColHex(color)
    self._line(x0,y0,x1,y1,color)
    

  def _fill_rect(self,x,y,w,h,color):
    xend = min(160,x+w)
    yend = min(160,y+h)
    x = max(x,0)
    y = max(y,0)
    w = xend-x
    h = yend-y
    for hh in range(h):
      for ww in range(w):
        self.bitmap[x+ww, y+hh] = color

  def _polygon(self,points,col):
    xs = []
    ys = []

    for point in points:
      xs.append(point[0])
      ys.append(point[1])

    x_offset = min(xs)
    y_offset = min(ys)

    for index, _ in enumerate(points):
      point_a = points[index]
      if index == len(points) - 1:
        point_b = points[0]
      else:
        point_b = points[index + 1]

      self._line(
        point_a[0],
        point_a[1],
        point_b[0],
        point_b[1],
        col,
      )

  def _round_rect_helper(self,x0,y0,r,color,x_offset,y_offset,stroke=1,corner_flags=0xf,fill=0):
    f = 1 - r
    ddF_x = 1
    ddF_y = -2 * r
    x = 0
    y = r
    
    while x < y:
      if f >= 0:
        y -= 1
        ddF_y += 2
        f += ddF_y
      x += 1
      ddF_x += 2
      f += ddF_x
      if corner_flags & 0x8:
        if fill:
          for w in range(x0 - y, x0 + y + x_offset):
            try:
              self.bitmap[w, y0 + x + y_offset] = fill
            except IndexError:
              pass
          for w in range(x0 - x, x0 + x + x_offset):
            try:
              self.bitmap[w, y0 + y + y_offset] = fill
            except IndexError:
              pass
        else:
          for line in range(stroke):
            try:
              self.bitmap[x0 - y + line, y0 + x + y_offset] = color
              self.bitmap[x0 - x, y0 + y + y_offset - line] = color
            except IndexError:
              pass
      if corner_flags & 0x1:
        if fill:
          for w in range(x0 - y, x0 + y + x_offset):
            try:
              self.bitmap[w, y0 - x] = fill
            except IndexError:
              pass
          for w in range(x0 - x, x0 + x + x_offset):
            try:
              self.bitmap[w, y0 - y] = fill
            except IndexError:
              pass
        else:
          for line in range(stroke):
            try:
              self.bitmap[x0 - y + line, y0 - x] = color
              self.bitmap[x0 - x, y0 - y + line] = color
            except IndexError:
              pass
      if corner_flags & 0x4:
        for line in range(stroke):
          try:
            self.bitmap[x0 + x + x_offset, y0 + y + y_offset - line] = color
            self.bitmap[x0 + y + x_offset - line, y0 + x + y_offset] = color
          except IndexError:
            pass
      if corner_flags & 0x2:
        for line in range(stroke):
          try:
            self.bitmap[x0 + x + x_offset, y0 - y + line] = color
            self.bitmap[x0 + y + x_offset - line, y0 - x] = color
          except IndexError:
            pass
          

  def _round_rect(self,x,y,width,height,r,color,fill=0,outline=0,stroke=1):
    # for i in range(0, width):  # draw the center chunk
    #   for j in range(r, height - r):  # draw the center chunk
    #     self.bitmap[x-r+i, y-r+j] = color
    self._round_rect_helper(
      x,
      y,
      r,
      color=color,
      fill=fill,
      x_offset=width - 2 * r - 1,
      y_offset=height - 2 * r - 1,
    )
    if outline:
      # draw flat sides
      for w in range(r, width - r):
        for line in range(stroke):
          self.bitmap[w, line] = 1
          self.bitmap[w, height - line - 1] = 1
      for _h in range(r, height - r):
        for line in range(stroke):
          self.bitmap[line, _h] = 1
          self.bitmap[width - line - 1, _h] = 1
      # draw round corners
      self._round_rect_helper(
          x,
          y,
          r,
          color=outline,
          stroke=stroke,
          x_offset=width - 2 * r - 1,
          y_offset=height - 2 * r - 1,
      )

  def _textBitmap(self,x0,y0,x,y,b,col,ext):
    for i in range(0,24,2):
      for j in range(7, -1, -1):
        if (b[i]>>j) & 0x1:
          #self.bitmap[x+7-j, y0] = col
          lsx=(x+7-j)*ext-(x0*(ext-1))
          lsy=y*ext-(y0*(ext-1))
          lsx=max(lsx,0)
          lsy=max(lsy,0)
          self.rect(lsx,lsy,ext,ext,col,1)
      for j in range(7, -1, -1):
        if (b[i+1]>>j) & 0x1:
          #self.bitmap[x+8+7-j, y] = col
          lsx=(x+8+7-j)*ext-(x0*(ext-1))
          lsy=y*ext-(y0*(ext-1))
          lsx=max(lsx,0)
          lsy=max(lsy,0)
          self.rect(lsx,lsy,ext,ext,col,1)
      y += 1


  def rect(self,x,y,w,h,color=255,fill=0):
    col = getColHex(color)
    if fill:
      self._fill_rect(x,y,w,h,col)
    else:
      self._fill_rect(x, y, w, 1, col)
      self._fill_rect(x, y + h- 1, w, 1, col)
      self._fill_rect(x, y, 1, h, col)
      self._fill_rect(x + w- 1, y, 1, h, col)

  def triangle(self,x0,y0,x1,y1,x2,y2,color=255,fill=0):
    color = getColHex(color)
    # Sort coordinates by Y order (y2 >= y1 >= y0)
    if y0 > y1:
      y0, y1 = y1, y0
      x0, x1 = x1, x0

    if y1 > y2:
      y1, y2 = y2, y1
      x1, x2 = x2, x1

    if y0 > y1:
      y0, y1 = y1, y0
      x0, x1 = x1, x0

    # Find the largest and smallest X values to figure out width for bitmap
    xs = [x0, x1, x2]
    points = [(x0, y0), (x1, y1), (x2, y2)]
    self._polygon(points,color)

    if fill:
      self._draw_filled(x0 , y0, x1 , y1, x2 , y2,color)

  def circle(self,x,y,r,color=255,fill=0):
    x += r
    y += r
    color = getColHex(color)
    if fill:
      fill = color
      if fill ==0 :
        fill = 1
      repairlinX = x-r*2
      repairlinY = y-r
      sum=0
      for i in range(r*2+1):
        try:
          self.bitmap[repairlinX+sum,repairlinY] = fill
        except IndexError:
          pass
        sum+=1
    self._round_rect(x-r,y-r,2*r+1,2*r+1,r,color,fill)

  def roundRect(self,x,y,r,w,h,fill=0,c=255):
    color = getColHex(c)
    if fill:
      fill = color
      if fill ==0 :
        fill = 1
    self._round_rect(x,y,w,h,r,color,fill)

  def text(self,text,x=0,y=0,ext=1,color=255):
    x0 = x
    y0 = y
    if type(text) == list:
      text = bytearray(text).decode()
    elif type(text) != str:
      text = str(text)
    for c in text:
      if c == '\n':
        y += 16
        x = x0
        continue
      o = ord(c)
      buf = espidf.flash_read(0x600000+o*24, 24)
      self._textBitmap(x0,y0,x,y,buf,color,ext)
      if o<160:
        x+=8
      else:
        x+=12

  def smartText(self,text,x=0,y=0,space=0,line=0,color=(255,255,255)):
    x = x
    y = y
    # self.fill((0, 0, 0))
    for i in text:
      self.text(i,x,y,1,color)
      x=x+12+space
      if x >= 154:
        x=0
        y=y+12+line
      if y > 128:
        break
      # if y < 0:
      #   continue

  def polygon(self,cx,cy,sides=3,r=10,th=3,rot=0,color=255,fill=0):
          if sides>60:
              sides = 60
          rads = 2*pi / sides
          XPoint=[]
          YPoint=[]
          deg = rot/180*pi
          for idx in range(sides):
              XPoint.append(int(cx + sin(idx*rads + deg) * r))
              YPoint.append(int(cy + cos(idx*rads + deg) * r))
          if fill:
              for idx in range(sides):
                  if idx+1 < sides:
                      self.triangle(cx,cy,XPoint[idx],YPoint[idx],XPoint[idx+1],YPoint[idx+1],color,fill)
                  else:
                      self.triangle(cx,cy,XPoint[idx],YPoint[idx],XPoint[0],YPoint[0],color,fill)

          if th:
              for n in range(th):
                  if n>0:
                      for idx in range(sides):
                          XPoint[idx] = int(cx + sin(idx*rads + deg) * (r-n))
                          YPoint[idx] = int(cy + cos(idx*rads + deg) * (r-n))
                  for idx in range(sides):
                      if idx+1<sides:
                          self.line(XPoint[idx],YPoint[idx],XPoint[idx+1],YPoint[idx+1], color)
                      else:
                          self.line(XPoint[idx],YPoint[idx],XPoint[0],YPoint[0], color)
          
  def loadimg(self,img,x,y):
    fp = open(img)
    if img.endswith(".jpg"):
      bitmaptools.loadjpg(self.bitmap,fp,x,y)
    else:
      bitmaptools.lodepng(self.bitmap,fp,x,y)

  def loadJpgBuff(self,buff,x,y):
    bitmaptools.loadjpg(self.bitmap,buff,x,y)


# if __name__ == '__main__':
#     s = Screen()
#     s.clear()
#     s.loadimg("images/yule-1.png",50,50)
#     while True:
#         pass
