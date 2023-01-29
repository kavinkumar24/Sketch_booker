from distutils.log import error
from typing import final
import cv2 #for image processing
import numpy as np #to store image
import sys
from PIL import Image
import streamlit as st
from pytesseract import image_to_string
import pytesseract
from PIL import UnidentifiedImageError
from streamlit_option_menu import option_menu
with st.sidebar:
    select = option_menu(
            menu_title="Main Menu",
            options = ["Pencil Scatcher","cartoon Image converter"],
            menu_icon="cast")
page_bg_img = f"""
        <style>
        .menu .container-xxl[data-v-4323f8ce]{{
            background-color:white;
            color:black; 
        }} 
        [data-testid="stSidebar"] {{
        background-color:#d5e1ed;
        color:white;    
        }}
        </style>
        """ 
st.markdown(page_bg_img, unsafe_allow_html=True)
base='light'  
    
st.image('sketch.png',width=300)

def pencilSketch(input_image):
    image_grey = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    image_invert = cv2.bitwise_not(image_grey)
    image_smoothing = cv2.GaussianBlur(
        image_invert, (21, 21), sigmaX=0, sigmaY=0)
    global final_image
    final_image = cv2.divide(image_grey, 255-image_smoothing, scale=256)
    return(final_image)

def cartoon(input_image):
        image_grey = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        image_invert = cv2.bitwise_not(image_grey)
        image_smoothing = cv2.GaussianBlur(
            image_invert, (71, 71), sigmaX=0, sigmaY=0)
        final_image = cv2.divide(image_grey, 255-image_smoothing, scale=256)
        smoothGrayScale = cv2.medianBlur(image_grey, 5)
        ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
        #plt.imshow(ReSized3, cmap='gray')
        getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 17, 10)
        ReSized4 = cv2.resize(getEdge, (800, 740))
        #plt.imshow(ReSized4, cmap='gray')
        colorImage = cv2.bilateralFilter(input_image, 9, 500, 500)
        ReSized5 = cv2.resize(colorImage, (1060, 840))
        #plt.imshow(ReSized5, cmap='gray')
        cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
        ReSized6 = cv2.resize(cartoonImage, (960, 540))
        #plt.imshow(ReSized6, cmap='gray'
        st.image(cartoonImage)
       
if select == 'Pencil Scatcher':
    st.title("PencilScatcher App")
    st.write('This web app is to help convert your photos to realistic Pencil Sketches')
    image = st.file_uploader("Upload your photo", type=['jpeg', 'jpg', 'png'])
    if image is None:
        st.write("You have not uploaded any image")
        st.write("Upload any type of images, but jpg images give better results")
    else:
        input_image = Image.open(image)
        final_img = pencilSketch(np.array(input_image))
        st.write("**Input Photo**")
        st.image(image, use_column_width=True)
        st.write("Output Pencil Photo")
        st.image(final_img, use_column_width=True)
        
if select == 'cartoon Image converter':
    image_cartoon = st.file_uploader("Upload your ", type=['jpeg', 'jpg'])
    if image_cartoon is None:
        st.header("support images only in jpg")
    else:
        try:
            st.image(image_cartoon)
            input_image = Image.open(image_cartoon)
            final_sketch = cartoon(np.array(input_image))
            st.write("**Input Photo**")
            st.image(final_sketch, use_column_width=True)
            st.write("Output Pencil Photo")
        except UnidentifiedImageError:
            st.caption('Converted')
