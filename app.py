from dotenv import load_dotenv
import streamlit as st
import time
from mvi_langchain import MomentoVectorIndex
from momento import VectorIndexConfigurations, CredentialProvider
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
load_dotenv()

st.title("💬 mvi-langchain-python-streamlit") 
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    db = MomentoVectorIndex(embedding_function=OpenAIEmbeddings(),
        configuration=VectorIndexConfigurations.Default.latest(),
        credential_provider=CredentialProvider.from_environment_variable("MOMENTO_AUTH_TOKEN"),
        index_name="state-of-the-union")
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
    response = qa_chain({"query": prompt})
    st.session_state.messages.append({
        "role": "assistant", "content": response['result']
    })
    st.chat_message("assistant").write(response['result'])