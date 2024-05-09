import streamlit as st
from utils import *
import constants


if 'HuggingFace_API_Key' not in st.session_state:
    st.session_state['HuggingFace_API_Key']=''
if 'Pinecone_API_Key' not in st.session_state:
    st.session_state['Pinecone_API_Key']=''


st.title('AI Help for Website')

st.session_state['HuggingFace_API_Key']= st.sidebar.text_input("Enter your HuggingFace API key",type="password")
st.session_state['Pinecone_API_Key']= st.sidebar.text_input("Enter your Pinecone API key",type="password")

import os
os.environ["PINECONE_API_KEY"] = st.session_state['Pinecone_API_Key']


load_button = st.sidebar.button("Load data to Pinecone", key="load_button")

if load_button:
    
    if st.session_state['HuggingFace_API_Key'] !="" and st.session_state['Pinecone_API_Key']!="" :

       
        site_data=get_website_data(constants.WEBSITE_URL)
        st.write("Data retrieved")

        #Split data into chunks
        
        chunks_data=split_data(site_data)
        st.write("Data Split")

        #Creating embeddings 
        embeddings=create_embeddings()
        st.write("Embeddings created")

        #Send data to Pinecone
        
        push_to_pinecone(st.session_state['Pinecone_API_Key'],constants.PINECONE_ENVIRONMENT,constants.PINECONE_INDEX,embeddings,chunks_data)
        st.write("Pushed data to Pinecone")

        st.sidebar.success("Data pushed to Pinecone successfully!")
    else:
        st.sidebar.error("Provide API keys")

prompt = st.text_input('Enter your query',key="prompt") 
document_count = st.slider('No.Of links to return - (0 LOW || 5 HIGH)', 0, 5, 2,step=1)

submit = st.button("Search") 


if submit:
    
    if st.session_state['HuggingFace_API_Key'] !="" and st.session_state['Pinecone_API_Key']!="" :

        #Creating embeddings 
        embeddings=create_embeddings()
        st.write("Embeddings instance creation done...")

        #Pull index data from Pinecone
        index=pull_from_pinecone(st.session_state['Pinecone_API_Key'],constants.PINECONE_ENVIRONMENT,constants.PINECONE_INDEX,embeddings)
        st.write("Pinecone index retrieved")

        #Fetch relavant documents from Pinecone index
        relavant_docs=get_similar_docs(index,prompt,document_count)
        st.write(relavant_docs)

        #Displaying results
        st.success("Please find the results :")
         #Displaying search results
        st.write("search results list....")
        for document in relavant_docs:
            
            st.write("**Result : "+ str(relavant_docs.index(document)+1)+"**")
            st.write("**Info**: "+document.page_content)
            st.write("**Link**: "+ document.metadata['source'])
       


    else:
        st.sidebar.error("Provide API keys")



