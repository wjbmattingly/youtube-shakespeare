import streamlit as st
import pandas as pd
from txtai.embeddings import Embeddings
import gdown
import os


def download_files():
    # a file
    url = "https://drive.google.com/file/d/1y7ZzHRXEyYkSWj3AH9-STUrxQcxaDt7I/view?usp=sharing"

    if os.path.exists("./models/shakespeare-index/embeddings"):
        pass
    else:
        output = "./models/shakespeare-index/embeddings"
        gdown.download(url, output, quiet=False, fuzzy=True)
        print("Download Complete")

download_files()
@st.cache(allow_output_mutation=True)
def load_txtai():
    embeddings = Embeddings({"path": "sentence-transformers/all-MiniLM-L6-v2"})
    embeddings.load("models/shakespeare-index")
    return embeddings
    
@st.cache(allow_output_mutation=True)
def load_df():
    df = pd.read_csv("data/shakespeare.csv")
    return df

st.title("Shakespeare Search Engine")
st.sidebar.image("images/shakespeare.png")
st.sidebar.markdown("Developed by [W.J.B. Mattingly](https://www.wjbmattingly.com) using [Streamlit](https://www.streamlit.io) and [txtAI](https://github.com/neuml/txtai).", unsafe_allow_html=True)
query = st.sidebar.text_input("Query")
num_results = st.sidebar.number_input("Number of Results", 1, 2000, 20)
ignore_search_words = st.sidebar.checkbox("Ignore Search Words")

embeddings = load_txtai()
df = load_df()

if st.sidebar.button("Search"):
    res = embeddings.search(query, num_results)
    indices = [index[0] for index in res]
    scores = [index[1] for index in res]
    y = df[df.index.isin(indices)]
    y["similarity"] = scores
    if ignore_search_words == True:
        words = query.split()
        for word in words:
            y = y[~y["PlayerLine"].str.contains(word.lower(), case=False)]
    st.table(y)
    