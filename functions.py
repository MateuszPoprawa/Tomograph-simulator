import math
import settings
import numpy as np
from  PIL import Image, ImageOps

def Bresenham_Algorithm_DA_X(x1, y1, x2, y2, image, view, illum = False):
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
    if(illum):
        illuminate(l, image, view)
    return l

def Bresenham_Algorithm_DA_Y(x1, y1, x2, y2, image, view, illum = False):
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
    if (illum) :
        illuminate(l, image, view)
    return l

def illuminate(l, image, view):
    for (x, y) in l:
        image.putpixel( (x, y), 255 )    
    view.image(image)

def create_sinogram(image, image_view, sinogram_view, progress):
    width, height = image.width, image.height
    im_matrix = np.array(ImageOps.grayscale(image))
    r = math.sqrt((width / 2) * (width / 2) + (height / 2) * (height / 2))
    sinogram = []
    j = 0
    for alpha in range(0, 360, settings.alpha_step):  
        sinogram.append([])               
        xe, ye = emiter_cord(r, alpha, height, width)
        for i in range(0, settings.n):
            xd, yd = detector_cord(r, alpha, height, width, i)
            points = calcualte_points(xe, ye, xd, yd, image, image_view)
            val = 0
            count = 0
            for (x, y) in points:
                val += im_matrix[y][x] 
                count += 1
            if count > 0:
                sinogram[j].append(val / count)
            else:
                sinogram[j].append(0)
        if settings.show_iterations:
            sinogram_view.image(Image.fromarray(np.array(sinogram)).convert("RGB").resize((width, height)))
        j += 1   
        progress.progress(j / (360 / settings.alpha_step * 2))
    sinogram_view.image(Image.fromarray(np.array(sinogram)).convert("RGB").resize((width, height)))
    if settings.filtering:
        sinogram = filter(sinogram)
    return sinogram

def backprojection(image, sinogram, view, progress):
    width, height = image.width, image.height
    im_matrix = np.zeros((height, width))
    r = math.sqrt((width / 2) * (width / 2) + (height / 2) * (height / 2))
    for j in range(0, len(sinogram)):
        alpha = j * settings.alpha_step               
        xe, ye = emiter_cord(r, alpha, height, width)
        for i in range(0, settings.n):
            xd, yd = detector_cord(r, alpha, height, width, i)
            points = calcualte_points(xe, ye, xd, yd, image, view)
            for (x, y) in points:
                im_matrix[y][x] += sinogram[j][i] 
        if settings.show_iterations:
            update_view(im_matrix, view)
        progress.progress((j + 1)/ (len(sinogram) * 2) + 0.5)
    return update_view(im_matrix, view)

def update_view(matrix, view):
    normalized_matrix = 255*(matrix - np.min(matrix))/(np.max(matrix) - np.min(matrix))
    img = Image.fromarray(normalized_matrix).convert("RGB")
    view.image(img)
    return img

def emiter_cord(r, alpha, height, width):
    xe = r * math.cos(math.radians(alpha)) + (width / 2)
    ye = (height / 2) - r * math.sin(math.radians(alpha))
    return xe, ye

def detector_cord(r, alpha,  height, width, i):
    xd = r * math.cos(math.radians(alpha) + math.pi - math.radians(settings.phi / 2) + math.radians(i * settings.phi / (settings.n - 1))) + (width / 2)
    yd = (height / 2) - r * math.sin(math.radians(alpha) + math.pi - math.radians(settings.phi / 2) + math.radians(i * settings.phi / (settings.n - 1)))
    return xd, yd

def calcualte_points(xe, ye, xd, yd, image, img_view, illuminate = False):
    if abs(xd - xe) > abs(yd - ye):
        points = Bresenham_Algorithm_DA_X(xe, ye, xd, yd, image, img_view, illuminate)
    else:
        points = Bresenham_Algorithm_DA_Y(xe, ye, xd, yd, image, img_view, illuminate)
    return points

def create_kernel():
    kernel = []
    start = -(settings.kernel_size - 1) / 2
    end = (settings.kernel_size - 1) / 2 + 1
    for k in range(int(start), int(end)):
        if k == 0:
            kernel.append(1)
        elif k % 2 == 0:
            kernel.append(0)
        else:
            kernel.append((-4 / (np.pi * np.pi)) / (k * k))
    return kernel

def filter(sinogram):
    kernel = create_kernel()
    for i in range(len(sinogram)):
        sinogram[i] = np.convolve(sinogram[i], kernel, mode="same")
    return sinogram

def MSE(image, backprojection_image):
    width, height = image.width, image.height
    mse = 0
    img1 = np.array(ImageOps.grayscale(image))
    img2 = np.array(ImageOps.grayscale(backprojection_image))
    for x in range(width):
        for y in range(height):
            mse += (int(img1[y][x]) - int(img2[y][x]))**2
    mse /= width * height
    print(mse)