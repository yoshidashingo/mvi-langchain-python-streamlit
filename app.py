from dotenv import load_dotenv
import os
import streamlit as st
import time

# For setting up the Momento Vector Index and langchain Vector Store
from mvi_langchain import MomentoVectorIndex
from momento import VectorIndexConfigurations, CredentialProvider
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.agents import AgentType, initialize_agent, load_tools

# For reading data and chunking it into smaller segments
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

# For doing QA
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import StreamlitCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler

load_dotenv()

def test():
    if os.environ.get('MOMENTO_AUTH_TOKEN') is None:
        raise ValueError("MOMENTO_AUTH_TOKEN is not set")

    if os.environ.get('OPENAI_API_KEY') is None:
        raise ValueError("OPENAI_API_KEY is not set")

    raw_documents = TextLoader('data/state-of-the-union.txt').load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)

    print(len(raw_documents))
    print(raw_documents[0].page_content[:500])

    db = MomentoVectorIndex(embedding_function=OpenAIEmbeddings(),
        configuration=VectorIndexConfigurations.Default.latest(),
        credential_provider=CredentialProvider.from_environment_variable("MOMENTO_AUTH_TOKEN"),
        index_name="state-of-the-union")

    _ = db.add_documents(documents=documents, ids=[f"sotu-chunk-{i}" for i in range(len(documents))])

    docs = db.similarity_search("What did the president say about small business?", k=2)
    print(len(docs))

    print(docs[0].page_content)
    print(docs[1].page_content)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

    result = qa_chain({"query": "What did the president say about small business?"})
    print(result)

    result = qa_chain({"query": "What did the president say about credit card fees?"})
    print(result)

    db._client.delete_index(index_name="state-of-the-union")

ENABLE_STREAMING_DELAY = True
STREAMING_DELAY_SEC = 0.01


st.title("mvi-langchain-python-streamlit")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(""):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        callbacks = []

        st_callback = StreamlitCallbackHandler(st.container())
        callbacks.append(st_callback)

        if ENABLE_STREAMING_DELAY:
            class DelayCallbackHandler(BaseCallbackHandler):
                def on_llm_new_token(self, token: str, **kwargs) -> None:
                    time.sleep(STREAMING_DELAY_SEC)

            delay_callback = DelayCallbackHandler()
            callbacks.append(delay_callback)

        response = st.session_state.agent.run(prompt, callbacks=callbacks)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})        