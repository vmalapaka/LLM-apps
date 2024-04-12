import streamlit as st
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(page_title="Similar Things", page_icon=":robot:")
st.header("Ask me something, I'll show you similar things")

embeddings = OpenAIEmbeddings()

from langchain.document_loaders.csv_loader import CSVLoader
loader = CSVLoader(file_path='myData.csv', csv_args={
    'delimiter': ',',
    'quotechar': '"',
    'fieldnames': ['Words']
    })

data = loader.load()

print(data)

db = FAISS.from_documents(data,embeddings)

def get_text():
    input_text = st.text_input("You:" , key=input)
    return input_text

user_input = get_text()
submit = st.button('Find Similar')

if submit:
    docs = db.similarity_search(user_input)
    st.subheader("Top Matches:")
    st.text(docs[0].page_content)
    st.text(docs[1].page_content)