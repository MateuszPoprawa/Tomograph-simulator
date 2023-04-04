import streamlit as st
import pandas as pd
from  PIL import Image, ImageDraw
import math
import functions
import settings

col1, col2, col3 = st.columns(3)
title = st.title("Symulator tomografu")

settings.alpha_step = st.sidebar.slider("Krok ∆α", 1, 60, 30)
settings.n = st.sidebar.slider("Liczba detektorów", 2, 90, 30)
settings.phi = st.sidebar.slider("Rozwartość/rozpiętość układu emiter/detektor", 1, 180, 60)

uploaded_file = st.sidebar.file_uploader("Choose a file", type=['png', 'jpg'])
sidebar_col1, sidebar_col2, sidebar_col3 = st.sidebar.columns(3)

if sidebar_col2.button('Start', type = "primary"):  
    if uploaded_file is not None:
        uploaded_image = Image.open(uploaded_file).convert("RGB")
        img_view = st.image(uploaded_image)
        copy = uploaded_image.copy()
        sinogram = functions.create_sinogram(copy, img_view)
        # img = Image.new("RGB", (uploaded_image.width, uploaded_image.height))
        # new_view = st.image(img)
        # functions.create_image(img, sinogram, new_view)