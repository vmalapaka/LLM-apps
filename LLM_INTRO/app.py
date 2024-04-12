import streamlit as st

from langchain.llms import OpenAI

#Taking question as input from user
def load_answer(question):
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct",temperature=0.7)

    answer=llm.invoke(question)
    return answer

#App UI
st.set_page_config(page_title="Question and Answers", page_icon=":robot:")
st.header("Question and Answers")

#Gets the user input
def get_text():
    input_text = st.text_input("Enter your question here: ", key="input")
    return input_text

user_input=get_text()
response = load_answer(user_input)

submit = st.button('Generate')  

#If generate button is clicked
if submit:

    st.subheader("Answer:")

    st.write(response)