import json
import requests
import base64
from pandasai.llm.local_llm import LocalLLM
import streamlit as st
import pandas as pd
from pandasai import Agent
import random
import sklearn
import langchain_groq
from dotenv import load_dotenv
import os
from streamlit_lottie import st_lottie

st.set_page_config(layout='wide')

load_dotenv()

from langchain_groq.chat_models import ChatGroq

model = ChatGroq(
    api_key = os.environ["GROQ_API_KEY"],
    model_name = "llama3-70b-8192"
)

# model = LocalLLM(
#     api_base="http://localhost:11434/v1",
#     model="llama3"
# )

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# lottie_coding = load_lottiefile("Lottiefile\\anim-1.json")

# st_lottie(lottie_coding, speed=1, width=300, height=300, key="initial", loop=True, quality="medium")

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background("img.png")



st.title("Hi I'M ALEXI \n Your AI Data Analyst")

with st.popover("Upload a File to Start"):
    uploaded_file= st.file_uploader("Choose a csv file", type="csv", key="file", help="Upload a csv file to get started", accept_multiple_files=False)
    if uploaded_file is not None:
        st.write("File uploaded successfully")
        # data = pd.read_csv(uploaded_file)
        # st.write(data.head(5))
        # st.write("First 5 rows")
messages = ["Generating...", "Hold on...", "Thinking...", "Loading...", "Processing..."]

if uploaded_file is not None:

    try:    
        data = pd.read_csv(uploaded_file, encoding='unicode_escape')
    except Exception as e:
        data = pd.read_csv(uploaded_file)

    st.write(data.head(5))
    st.write("First 5 rows")

    agent = Agent(data, config={"llm": model})
    prompt = st.text_area("Lets talk with the data: ")
    
    if st.button("Ask"):
        if prompt:
            with st.spinner(random.choice(messages)):

                st.write(agent.chat(prompt))






