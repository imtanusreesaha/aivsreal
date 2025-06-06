# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zQmOz3Ep327nLr5yOutahPsA93aClgiM
"""

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import requests

st.set_page_config(
    page_title="ProofPixel",
    page_icon="🤖"
)

st.title('ProofPixel:Real and AI-Generated Image Detection Using Modified Xception Net Architecture')

# ✅ Corrected GitHub raw model URL (no quotes or duplication in assignment)
github_model_url = "https://raw.githubusercontent.com/imtanusreesaha/CUSTOMXCEPTIONET224/d800c4b3bbfc26e5c523e6643392229836f7cefb/customxception224.h5"

# ✅ Cache the model loading
@st.cache_resource
def load_model(github_model_url):
    response = requests.get(github_model_url)
    with open("customxceptionet224.h5", "wb") as f:
        f.write(response.content)
    model = tf.keras.models.load_model("customxceptionet224.h5")
    return model

model = load_model(github_model_url)

def classify_image(file_path):
    image = Image.open(file_path)
    image = image.resize((32, 32))
    img = np.asarray(image)
    img = np.expand_dims(img / 255.0, axis=0)
    predictions = model.predict(img)
    return 'REAL' if predictions > 0.5 else 'AI-GENERATED IMAGE'

st.write("Upload an image to check whether it is an AI-Generated Image or a Real Image.")

file_uploaded = st.file_uploader("Choose the Image File", type=["jpg", "jpeg"])

if st.button('Check', use_container_width=True):
    if file_uploaded is not None:
        res = classify_image(file_uploaded)
        c1, buff, c2 = st.columns([2, 0.5, 2])
        c1.image(file_uploaded, use_column_width=True)
        c2.subheader("Classification Result")
        c2.write(f"The image is classified as **{res.title()}**.")
    else:
        st.error('Please upload an image to verify.', icon="❌")

