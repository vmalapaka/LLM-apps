import streamlit as st
from utils import *
from dotenv import load_dotenv

if 'HR_tickets' not in st.session_state:
    st.session_state['HR_tickets'] =[]
if 'IT_tickets' not in st.session_state:
    st.session_state['IT_tickets'] =[]
if 'Transport_tickets' not in st.session_state:
    st.session_state['Transport_tickets'] =[]

def main():
    
    load_dotenv()
    st.header("Automatic Ticket Classification Tool")
    #Capture user input
    st.write("Enter your query:")
    
    user_input = st.text_input("Search")

    if user_input:

        #creating embeddings 
        embeddings=create_embeddings_load_data()

        #Function to pull index data from Pinecone
        import os
        os.environ["PINECONE_API_KEY"] = "50b78f61-9dee-49b1-af4e-131a7f73ccdc"
        
        index=pull_from_pinecone(os.getenv("PINECONE_API_KEY"),"us-east-1","document",embeddings)
        
        #To fetch the top relevent documents from our vector store - Pinecone Index
        relavant_docs=get_similar_docs(index,user_input)

        #Return the fine tuned response by LLM
        response=get_answer(relavant_docs,user_input)
        st.write(response)

        
        #Button to create a ticket with classification
        button = st.button("Submit a ticket")

        if button:
            
            embeddings = create_embeddings_load_data()
            query_result = embeddings.embed_query(user_input)

            #loading the ML model, so that we can use it to predit the class to which this ticket belongs to
            department_value = predict(query_result)
            st.write("Ticket has been sumbitted to : "+department_value)

            #Appending the tickets to below list, so that we can view/use them later on...
            if department_value=="HR":
                st.session_state['HR_tickets'].append(user_input)
            elif department_value=="IT":
                st.session_state['IT_tickets'].append(user_input)
            else:
                st.session_state['Transport_tickets'].append(user_input)



if __name__ == '__main__':
    main()


    