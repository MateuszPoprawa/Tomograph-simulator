import streamlit as st
import pandas as pd
from  PIL import Image, ImageOps
import math
import functions
import settings
import save_dicom
from numpy import array
from pydicom import dcmread

def run():
    uploaded_image = Image.open(uploaded_file)
    blank_img = Image.new("RGB", (uploaded_image.width, uploaded_image.height))
    img_view = col1.image(uploaded_image)
    new_view = col2.image(blank_img)
    progress = st.progress(0.0)
    sinogram = functions.create_sinogram(uploaded_image, img_view, new_view, progress)
    backprojection_img = functions.backprojection(blank_img, sinogram, new_view, progress)
    progress.empty()
    if settings.save_as_dicom:
        save_dicom.save_as_dicom(patient_data['PatientID'], array(ImageOps.grayscale(backprojection_img)), patient_data)
    
def config():
    settings.alpha_step = st.sidebar.slider("Krok ∆α", 1, 10, 5)
    settings.n = st.sidebar.slider("Liczba detektorów", 10, 360, 180)
    settings.phi = st.sidebar.slider("Rozwartość/rozpiętość układu emiter/detektor", 10, 180, 90)
    settings.show_iterations = st.sidebar.checkbox("Pokaż kroki pośrednie")
    save_as_dicom = st.sidebar.checkbox("Zapisz jako DICOM")
    settings.save_as_dicom = False
    if save_as_dicom:
        show_expander()
        settings.save_as_dicom = True

def show_expander():
    with st.sidebar.expander("Dane DICOM", True):
        patient_data['PatientName'] = st.text_input("Imię pacjenta")
        patient_data['PatientID'] = st.text_input("ID pacjenta")
        patient_data['ImageComments'] = st.text_input("Komentarz")
        patient_data['Date'] = st.date_input("Data badania")

patient_data = {}

simulation_tab, dicom_tab = st.tabs(["Symulacja", "Odczyt DICOM"])

with simulation_tab:
    st.header("Symulator tomografu")
    col1, col2 = st.columns(2)

with dicom_tab:
    st.header("Odczyt pliku DICOM")
    dcm_file = st.file_uploader("Wybierz plik", type=['dcm'])
    image_tab, data_tab = st.tabs(["Obraz", "Dane"])
    if dcm_file is not None:
        dcm = dcmread(dcm_file)
        with image_tab:
            st.image(dcm.pixel_array)
        with data_tab:
            st.text(dcm)

config()

uploaded_file = simulation_tab.file_uploader("Wybierz plik", type=['png', 'jpg'])
sidebar_col1, sidebar_col2, sidebar_col3 = st.sidebar.columns(3)

if sidebar_col2.button('Start', type = "primary"):  
    if uploaded_file is not None:       
        if not settings.save_as_dicom or "" not in patient_data.values():
            run()
        else:
            simulation_tab.info("Uzupełnij informacje")
    else:
        simulation_tab.info("Wybierz plik")