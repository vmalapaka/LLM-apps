import streamlit as st
from utils import generate_script

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #0099ff;
        color : #ffffff;   
    }
    div.stButton > button:hover {
        background-color: #00ff00;
        color : #FFFFFF;   
    }
    </style>""",unsafe_allow_html = True)


if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] = ''

st.title('Youtube Script Generation')

st.sidebar.title('API Key 🔑 ')

st.session_state['API_Key'] = st.sidebar.text_input("What's your API key?", type='password')


prompt = st.text_input('Provide the topic of the video',key="prompt")  
video_length = st.text_input('Expected Video Length 🕒 (in min)',key="video_length")  
creativity = st.slider('Creativity limit ✨ - (0 LOW || 1 HIGH)', 0.0, 1.0, 0.2,step=0.1)

submit = st.button("Generate Script for me")


if submit:
    
    if st.session_state['API_Key']:
        search_result,title,script = generate_script(prompt,video_length,creativity,st.session_state['API_Key'])
        st.success('Here is the requested script')

        st.subheader("Title:")
        st.write(title)

        st.subheader("Your Video Script:📝")
        st.write(script)

        st.subheader("Check Out - DuckDuckGo Search:🔍")
        with st.expander('Show more'): 
            st.info(search_result)
    else:
        st.error("Please provide API key.....")

