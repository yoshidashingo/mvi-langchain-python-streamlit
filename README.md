# The RAG App workshop for Momento Vector Index
>  Momento Vector Index example for handson using Python, LangChain, OpenAI and Streamlit.

This repository is originally made for ServerlessDays Tokyo 2023 Momento Hands-on Workshop

## Features
- RAG(Retrieval Augmented Generation) web app.
- Getting embeddings(vector data) from local file using OpenAI Embeddings API.
- Hosted the vector data to Momento Vector Index and retrieve from it.
- Cached the Q&A histories to Momento Cache.
- Answer generated using OpenAI.
- UI was created using Streamlit.

## Getting Started
1. Copy `.env.template` to `.env`.
2. Get and fill the API key to `MOMENTO_AUTH_TOKEN` and `OPENAI_API_KEY` in `.env`.
3. Change the source data in `data/sample.txt`.
4. Create virtual environment

```sh
python3 -m venv .venv
. .venv/bin/activate
```

5. Install the libraries.
```sh
$ pip install -r requirements.txt
```

6. Generate vector data

```
python insert.py
```

7. Run streamlit, Access to `http://localhost:8051` and ask sometiong about your data
```sh
streamlit run app.py
```

8. Delete vector data

```sh
python delete.py
```

## Feedback
You are welcome to discuss it on our discord.
