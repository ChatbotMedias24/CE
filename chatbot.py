import streamlit as st
from dotenv import load_dotenv
import pickle
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import toml
import docx2txt



# Sidebar contents
textcontainer = st.container()
with textcontainer:
    logo_path = "medi.png"
    logoo_path = "cp.png"
    st.sidebar.image(logo_path,width=200)
    st.sidebar.image(logoo_path,width=150)
    
st.sidebar.subheader("Suggestions:")
questions = [
        "Donne moi un résumé du rapport ",
        "Quels sont les secteurs économiques qui ont connu la plus forte croissance des exportations en 2022 ?",
        "Quels sont les principaux défis auxquels est confronté le commerce extérieur du Maroc en 2022 ?",
        "Comment les échanges commerciaux du Maroc avec les pays membres de l'Union européenne ont-ils évolué depuis la sortie du Royaume-Uni de l'UE en 2021 ?"
    ]    
 
load_dotenv(st.secrets["OPENAI_API_KEY"])
 
def main():
    st.header("Rapport commerce extérieur du maroc 2022 💬")
    # upload a PDF file
    docx = 'CE.docx'
 
    # st.write(pdf)
    if docx is not None:
        text = docx2txt.process(docx)
         # Get the first page as an image
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
            )
        chunks = text_splitter.split_text(text=text)
 
        # # embeddings
        # st.write(chunks)
 
        embeddings = OpenAIEmbeddings()
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        with open("aaa.pkl", "wb") as f:
            pickle.dump(VectorStore, f)
 
        # embeddings = OpenAIEmbeddings()
        # VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        
        selected_questions = st.sidebar.radio("****Choisir :****",questions)
    
        if selected_questions:
           query = st.text_input("Selected Question:", selected_questions)
        else :
           query = st.text_input("Ask questions about your PDF file:")
        # st.write(query)
 
        if query:
            docs = VectorStore.similarity_search(query=query, k=3)
 
            llm = OpenAI()
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                print(cb)
            st.write(response)

if __name__ == '__main__':
    main()
