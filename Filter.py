import cv2
import numpy as np
import streamlit as st
from PIL import Image

def black_white(img):
    grey_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return grey_img

def brightness(img, level):
    bright_img = cv2.convertScaleAbs(img, alpha=1, beta=level)  # تعديل `alpha`
    return bright_img

def style_img(img, sigma_s=10, sigma_r=0.1):
    blur_img = cv2.GaussianBlur(img, (9, 9), 0)
    stylized_img = cv2.stylization(blur_img, sigma_s=sigma_s, sigma_r=sigma_r)
    return stylized_img

def HDR(img, level, sigma_s=10, sigma_r=0.1):
    bright = cv2.convertScaleAbs(img, alpha=1, beta=level)  # تعديل `alpha`
    hd_img = cv2.detailEnhance(bright, sigma_s=sigma_s, sigma_r=sigma_r)
    return hd_img

def vintage(img, level=2):
    height, width = img.shape[:2]
    x_kernel = cv2.getGaussianKernel(width, width / level)
    y_kernel = cv2.getGaussianKernel(height, height / level)
    kernel = x_kernel.T * y_kernel
    mask = kernel / kernel.max()
    copy_img = np.copy(img)
    
    for i in range(3):  
        copy_img[:, :, i] = copy_img[:, :, i] * mask  # تطبيق القناع على كل قناة
    
    return copy_img.astype(np.uint8)  # التأكد من أن الصورة صحيحة

# 🎨 🎨 Streamlit UI 🎨 🎨
st.title('🖼️ Image Filter App')

uploader = st.file_uploader("📤 Upload an image", type=['png', 'jpg', 'jpeg'])

if uploader is not None:
    img = Image.open(uploader)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # التأكد من أن الصورة في ترتيب BGR
    original_img, output_img = st.columns(2)

    with original_img:
        st.header("📌 Original Image")
        st.image(img, channels='BGR')

    st.header("🎭 Apply Filters")
    options = st.selectbox("🎨 Select a Filter:", ('None', 'black_white', 'brightness', 'style_img', 'HDR', 'vintage'))

    output_flag = True
    color = 'BGR'

    if options == 'None':
        output_flag = False
        output = img
    elif options == 'black_white':
        output = black_white(img)
        color = 'GRAY'
    elif options == 'brightness':
        level = st.slider('🔆 Brightness Level:', -50, 50, 10, step=5)
        output = brightness(img, level)
    elif options == 'style_img':
        sigma_s = st.slider('🔹 Sigma_s:', 0, 200, 100, step=5)
        sigma_r = st.slider('🔸 Sigma_r:', 0.01, 1.0, 0.1, step=0.01)
        output = style_img(img, sigma_s=sigma_s, sigma_r=sigma_r)
    elif options == 'HDR':
        level = st.slider('⚡ HDR Level:', 0, 100, 30, step=5)
        output = HDR(img, level)
    elif options == 'vintage':
        level = st.slider('📜 Vintage Effect Level:', 1, 10, 2, step=1)
        output = vintage(img, level)

    with output_img:
        st.header("🖼️ Filtered Image")
        if output_flag:
            if color == "BGR":
                output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
            st.image(output, channels=color)