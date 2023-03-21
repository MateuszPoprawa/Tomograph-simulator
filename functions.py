import math

def Bresenham_Algorithm_DA_X(x1, y1, x2, y2, image, view):
    m = 1024
    dx = m * (x2 - x1)
    dy = m * (y2 - y1)
    i1 = math.floor(x1)
    i2 = math.floor(x2)
    j = math.floor(y1)
    e = math.floor( dy * ( 1 - (x1 - i1) ) - dx * (1 - y1 - j) )
    l = []
    for i in range(i1, i2):
        if i >= 0 and j >= 0 and i < image.width and j < image.height:
            l.append((i, j))
        if i % 1000 == 0:
            illuminate(l, image, view)
            l = []
        if (e > 0):
            j += 1
            e -= dx
        e += dy
    illuminate(l, image, view)

def Bresenham_Algorithm_DA_Y(x1, y1, x2, y2, image, view):
    dx = (x2 - x1)
    dy = (y2 - y1)
    m = abs(dx / dy)
    i = math.floor(x1)
    j1 = math.floor(y1)
    j2 = math.floor(y2)
    l = []
    if dx > 0:
        inc = 1
        e = -(1 - (x1 - i) - (y1 -j1) * (dx / dy))
    else:
        inc = -1
        e = -((x1 - i) - (y1 -j1) * (dx / dy))
    for j in range(j1, j2):
        while e >= 0:
            i += inc
            e -= 1.0
        if i >= 0 and j >= 0 and i < image.width and j < image.height:
            l.append((i, j))
        if i % 1000 == 0:
            illuminate(l, image, view)
            l = []
        j += inc
        e += m
    illuminate(l, image, view)

def illuminate(l, image, view):
    for (x, y) in l:
        image.putpixel( (x, y), 255 )    
    view.image(image)