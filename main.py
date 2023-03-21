import streamlit as st
import pandas as pd
from  PIL import Image, ImageDraw
import math
import functions
import settings

col1, col2, col3 = st.columns(3)
title = st.title("Tomograph simulator")


uploaded_file = st.sidebar.file_uploader("Choose a file", type=['png', 'jpg'])
sidebar_col1, sidebar_col2, sidebar_col3 = st.sidebar.columns(3)

if sidebar_col2.button('Start', type = "primary"):  
    if uploaded_file is not None:
        uploaded_image = Image.open(uploaded_file).convert("RGB")
        img = st.image(uploaded_image)
        width = uploaded_image.width
        height = uploaded_image.height
        r = math.sqrt((width / 2) * (width / 2) + (height / 2) * (height / 2))
        copy = uploaded_image.copy()
        for alpha in range(0, 360, settings.alpha_step):                     
            xe = r * math.cos(math.radians(alpha)) + (width / 2)
            ye = (height / 2) - r * math.sin(math.radians(alpha))
            for i in range(0, settings.n):
                xd = r * math.cos(math.radians(alpha) + math.pi - math.radians(settings.phi / 2) + math.radians(i * settings.phi / (settings.n - 1))) + (width / 2)
                yd = (height / 2) - r * math.sin(math.radians(alpha) + math.pi - math.radians(settings.phi / 2) + math.radians(i * settings.phi / (settings.n - 1)))
                if abs(xd - xe) > abs(yd - ye):
                    functions.Bresenham_Algorithm_DA_X(xe, ye, xd, yd, copy, img)
                else:
                    functions.Bresenham_Algorithm_DA_Y(xe, ye, xd, yd, copy, img)