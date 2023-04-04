import math
import settings

def Bresenham_Algorithm_DA_X(x1, y1, x2, y2, image, view):
    dx = x2 - x1
    dy = y2 - y1
    m = abs(dy / dx)
    if dx > 0:
        x_inc = 1
    else:
        x_inc = -1
    if dy > 0:
        y_inc = 1
    else:
        y_inc = -1
    i1 = math.floor(x1)
    i2 = math.floor(x2)
    j = math.floor(y1)
    e =  -(1 - (y1 - j) - (dy*(1 - (x1 - i1))) / dx)
    l = []
    for i in range(i1, i2, x_inc):
        if i >= 0 and j >= 0 and i < image.width and j < image.height:
            l.append((i, j))
        if (e >= 0):
            j += y_inc
            e -= 1.0
        e += m
    #illuminate(l, image, view)
    return l

def Bresenham_Algorithm_DA_Y(x1, y1, x2, y2, image, view):
    dx = x2 - x1
    dy = y2 - y1
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
    if dy > 0:
        y_inc = 1
    else:
        y_inc = -1
    for j in range(j1, j2, y_inc):
        while e >= 0:
            i += inc
            e -= 1.0
        if i >= 0 and j >= 0 and i < image.width and j < image.height:
            l.append((i, j))
        j += inc
        e += m
    #illuminate(l, image, view)
    return l

def illuminate(l, image, view):
    for (x, y) in l:
        image.putpixel( (x, y), 255 )    
    view.image(image)

def create_sinogram(image, img_view):
    width = image.width
    height = image.height
    r = math.sqrt((width / 2) * (width / 2) + (height / 2) * (height / 2))
    sinogram = []
    for alpha in range(0, 360, settings.alpha_step):                     
        xe = r * math.cos(math.radians(alpha)) + (width / 2)
        ye = (height / 2) - r * math.sin(math.radians(alpha))
        for i in range(0, settings.n):
            xd = r * math.cos(math.radians(alpha) + math.pi - math.radians(settings.phi / 2) + math.radians(i * settings.phi / (settings.n - 1))) + (width / 2)
            yd = (height / 2) - r * math.sin(math.radians(alpha) + math.pi - math.radians(settings.phi / 2) + math.radians(i * settings.phi / (settings.n - 1)))
            print(ye, yd)
            if abs(xd - xe) > abs(yd - ye):
                points = Bresenham_Algorithm_DA_X(xe, ye, xd, yd, image, img_view)
            else:
                points = Bresenham_Algorithm_DA_Y(xe, ye, xd, yd, image, img_view)
            sum = (0, 0, 0)
            count = 0
            for (x, y) in points:
                color = image.getpixel((x,y))
                sum = tuple(map(lambda i, j: i + j, sum, color))
                count += 1
            sinogram.append([alpha, tuple(map(lambda i: i / count, sum))])
    return sinogram

def create_image(image, sinogram, img_view):
    width = image.width
    height = image.height
    r = math.sqrt((width / 2) * (width / 2) + (height / 2) * (height / 2))
    for alpha, (r, g, b) in sinogram:                   
        xe = r * math.cos(math.radians(alpha)) + (width / 2)
        ye = (height / 2) - r * math.sin(math.radians(alpha))
        for i in range(0, settings.n):
            xd = r * math.cos(math.radians(alpha) + math.pi - math.radians(settings.phi / 2) + math.radians(i * settings.phi / (settings.n - 1))) + (width / 2)
            yd = (height / 2) - r * math.sin(math.radians(alpha) + math.pi - math.radians(settings.phi / 2) + math.radians(i * settings.phi / (settings.n - 1)))
            if abs(xd - xe) > abs(yd - ye):
                points = Bresenham_Algorithm_DA_X(xe, ye, xd, yd, image, img_view)
            else:
                points = Bresenham_Algorithm_DA_Y(xe, ye, xd, yd, image, img_view)
            for (x, y) in points:
                image.putpixel( (x, y), (int(r), int(g) ,int(b)) )
    img_view.image(image)