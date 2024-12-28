import os, tempfile
from PIL import Image
import streamlit as st
from utils import detect_and_process_id_card


st.set_page_config(page_title='ID Egyption Card', page_icon='💳', layout='wide')
st.title('ID Egyption Card 💳')


uploaded_file = st.sidebar.file_uploader("Upload an ID card image",
                                        type=['webp', 'jpg', 'tif', 'tiff', 'png', 'mpo', 'bmp', 'jpeg', 'dng', 'pfm'])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
        
    image = Image.open(temp_file_path)
    
    st.subheader('ID Egyptian Card 💳')
    st.sidebar.image(image)
    
    try:
        # Call the detect_and_process_id_card function
        first_name, second_name, Full_name, national_id, address, birth, gov, gender = detect_and_process_id_card(temp_file_path)
        st.image(Image.open("d2.jpg"), use_container_width=True)
        st.markdown("---")
        st.write(f"First Name: {first_name}")
        st.write(f"Second Name: {second_name}")
        st.write(f"Full Name: {Full_name}")
        st.write(f"National ID: {national_id}")
        st.write(f"Address: {address}")
        st.write(f"Birth Date: {birth}")
        st.write(f"Governorate: {gov}")
        st.write(f"Gender: {gender}")

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        os.remove(temp_file_path)