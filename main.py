import streamlit as st
from PIL import Image
from io import BytesIO

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db

import base64
import time
import requests
import os
from datetime import datetime


cred2 = credentials.Certificate(r"C:\Users\Blnd\Desktop\dd\sassa.json")
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred2, {
        'databaseURL': 'https://sasa-6f227-default-rtdb.firebaseio.com/'
    })


st.set_page_config(page_title="chatting", initial_sidebar_state="auto", layout="centered")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
footer {
    visibility: hidden;
}
footer:after {
    content:'Made by 4S group';
    visibility: visible;
    display: block;
    position: relative;
    #background-color: red;
    padding: 5px;
    top: 2px;
}
</style>
"""

iii = r"C:\Users\Blnd\Desktop\dd\ll.png"
image4 = Image.open(iii)

st.sidebar.image(image4)
st.sidebar.subheader("Welcome")
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

name = st.sidebar.text_input("Name")
password = st.sidebar.text_input("Password", type="password")
st.sidebar.button("Log-in")
def Home():


    if password == "":

        current_datetime = datetime.now()
        d = current_datetime.strftime("%d/%m/%Y")
        d = d.replace("/", " ")
        st.header("Hii, how was your day")
        st.subheader(f"today is {d}")
        day = st.text_area("Talk about your day to your friends😃", height=1000)

        fil = st.file_uploader('Uplode image or file if needed')


        a = st.button("submit")
        if a:
            reff = firebase_db.reference()

            file_content = None
            encoded_file = None
            file_name = None

            if fil is not None:
                file_content = fil.read()
                # Encode the file content to base64
                encoded_file = base64.b64encode(file_content).decode('utf-8')
                file_name = fil.name

            # Create the data to be saved
            data_to_save = {
                "day": day,
            }

            # Add file details if a file is uploaded
            if file_content:
                data_to_save["file_name"] = file_name
                data_to_save["file_content"] = encoded_file

            # Save the data to Firebase
            reff.child("story").child(name).child(d).set(data_to_save)

            st.success("Your day has successfully submitted!")

def ViewDay():
    st.header("See how was your friends day")
    re = firebase_db.reference("story")
    stories = re.get()

    # Get the keys (which represent different stories) to populate the selectbox
    story_keys = list(stories.keys()) if stories else []

    # Selectbox to choose a story
    nn = st.selectbox("Select your friend", story_keys)
    date_to_view = st.date_input("Select a date")
    d = date_to_view.strftime("%d %m %Y")

    if st.button("see"):
        reff = firebase_db.reference()
        data = reff.child("story").child(nn).child(d).get()

        if data:
            st.subheader(f"Entry for {d}:")
            st.write(data.get("day", "No entry for this day."))

            # Check if there's a file associated with this entry
            if "file_name" in data and "file_content" in data:
                st.subheader("Attached File:")
                file_name = data["file_name"]
                file_content = base64.b64decode(data["file_content"])

                # Display or download the file based on its type
                if file_name.endswith(('jpg', 'jpeg', 'png')):
                    st.image(Image.open(BytesIO(file_content)), caption=file_name)
                else:
                    st.download_button(label=f"Download {file_name}", data=file_content, file_name=file_name)
        else:
            st.warning(f"No entry found for {d}.")








page_names_to_funcs = {
    "Talk about your day😁": Home,
    "See how was your friend day😉": ViewDay
}

selected_page = st.sidebar.selectbox("Select the service you want", list(page_names_to_funcs.keys()))
page_names_to_funcs[selected_page]()