import streamlit as st
from dotenv import load_dotenv
from utils import query_agent

load_dotenv()

st.title("CSV Analysis Tool")
st.header("Upload your csv file here:")

data = st.file_uploader("Upload CSV File", type = "csv")

query = st.text_area("Enter your query here:")
button = st.button("Generate response")

if button:
    answer = query_agent(data,query)
    st.write(answer)
