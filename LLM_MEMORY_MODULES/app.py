from langchain_community.chat_models import ChatOpenAI
import streamlit as st 
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
                                                  ConversationSummaryMemory, 
                                                  ConversationBufferWindowMemory
                                                  )

import tiktoken
from langchain.memory import ConversationTokenBufferMemory

if 'conversation' not in st.session_state:
    st.session_state['conversation'] =None
if 'messages' not in st.session_state:
    st.session_state['messages'] =[]
if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] =''

st.set_page_config(page_title="Chat with me")
st.markdown("<h1 style= 'text_align : center;'>How can I assist you? </h1>", unsafe_allow_html = True)

st.sidebar.title("API")
st.session_state['API_Key'] = st.sidebar.text_input("Enter you API key",type = "password")
summarise_button = st.sidebar.button("Summarise",key = "summarise")
if summarise_button:
    summarise_placeholder = st.sidebar.write("Thanks for chatting \n\n"+st.session_state['conversation'].memory.buffer)

response_container = st.container()
container = st.container()



def get_response(User_input,api_key):

    if st.session_state['conversation'] is None:

        llm = ChatOpenAI(
            temperature=0,
            openai_api_key = api_key,
            model_name='gpt-3.5-turbo-0125'  
        )
        
        st.session_state['conversation'] = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationSummaryMemory(llm=llm)
        )
        
    response = st.session_state['conversation'].predict(input=User_input)

    return response



with container:
    with st.form(key="my_form", clear_on_submit = True):
        user_input = st.text_area("Your question goes here:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')
        if submit_button:
            st.session_state['messages'].append(user_input)
            model_response = get_response(user_input,st.session_state['API_Key'])
            st.session_state['messages'].append(model_response)
            st.write(st.session_state['messages'])
            with response_container:
                for i in range(len(st.session_state['messages'])):
                        if (i % 2) == 0:
                            message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                        else:
                            message(st.session_state['messages'][i], key=str(i) + '_AI')




