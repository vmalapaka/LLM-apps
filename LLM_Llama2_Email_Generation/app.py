import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers

st.set_page_config(page_title="Generate Emails", layout='centered', initial_sidebar_state='collapsed')
st.header("Generate Emails")

def getLLMResponse(form_input,email_sender,email_recipient,email_style):
    

    llm = CTransformers(model='llama-2-7b-chat.ggmlv3.q8_0.bin',     
                    model_type='llama',
                    config={'max_new_tokens': 256,
                            'temperature': 0.01})
    template = """
    Draft an email with {style} style and includes topic :{email_topic}.\n\nSender: {sender}\nRecipient: {recipient}
    \n\nEmail Text:
    
    """

    #Creating PROMPT
    prompt = PromptTemplate(
    input_variables=["style","email_topic","sender","recipient"],
    template=template,)

    response=llm.invoke(prompt.format(email_topic=form_input,sender=email_sender,recipient=email_recipient,style=email_style))
    print(response)

    return response

form_input = st.text_area('Enter the email topic',height=275)

col1,col2,col3 = st.columns([10,10,5])
with col1:
    email_sender= st.text_input("Enter Sender name")

with col2:
    email_recipient= st.text_input("Enter Receiver name")

with col3:
    email_style = st.selectbox('Writing Style',('Formal','Appreciating','Not Satisfied','Neutral'), index=0)

submit = st.button('Generate')

if submit:
    st.write(getLLMResponse(form_input,email_sender,email_recipient,email_style))
