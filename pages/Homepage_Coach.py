#font use Playfair
import streamlit as st
import base64

def set_background_1():
    """
    Set the background of the Streamlit app using a locally stored image.
    """
    image_path = 'Coach.png'  # Update this path when new image is created
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """

    st.markdown(background_style, unsafe_allow_html=True)
set_background_1()