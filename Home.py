import streamlit as st
import pandas as pd
from txtai.embeddings import Embeddings
import gdown
import os


def download_files():
    # url = "https://drive.google.com/file/d/1y7ZzHRXEyYkSWj3AH9-STUrxQcxaDt7I/view?usp=sharing"
    #
    # if os.path.exists("./models/shakespeare-index/embeddings"):
    #     pass
    # else:
    #     output = "./models/shakespeare-index/embeddings"
    #     gdown.download(url, output, quiet=False, fuzzy=True)

    url_full = "https://drive.google.com/file/d/1ySyspDK7g1DQIVbegpDOpwv9FH73smiB/view?usp=sharing"

    if os.path.exists("./models/shakespeare-index/embeddings"):
        pass
    else:
        output = "./models/shakespeare-index-full/embeddings"
        gdown.download(url_full, output, quiet=False, fuzzy=True)
        print("Download Complete")

download_files()
@st.cache(allow_output_mutation=True)
def load_txtai():
    embeddings = Embeddings({"path": "sentence-transformers/all-MiniLM-L6-v2", "content": True})
    embeddings.load("models/shakespeare-index-full")
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

def create_html(result):
    output = f""
    spans = []
    for token, score in result["tokens"]:
        color = None
        if score >= 0.1:
            color = "#fdd835"
        elif score >= 0.075:
            color = "#ffeb3b"
        elif score >= 0.05:
            color = "#ffee58"
        elif score >= 0.02:
            color = "#fff59d"

        spans.append((token, score, color))

    if result["score"] >= 0.05 and not [color for _, _, color in spans if color]:
        mscore = max([score for _, score, _ in spans])
        spans = [(token, score, "#fff59d" if score == mscore else color) for token, score, color in spans]

    for token, _, color in spans:
        if color:
            output += f"<span style='background-color: {color}'>{token}</span> "
        else:
            output += f"{token} "
    return output


if st.sidebar.button("Search"):
    res = embeddings.explain(query, limit = num_results)
    html_txt = [create_html(r) for r in res]
    indices = [int(index['id']) for index in res]
    scores = [index['score'] for index in res]
    texts = [index['text'] for index in res]
    y = df.iloc[indices]
    y['PlayerLine'] = html_txt
    # y = df[df.index.isin(indices)].drop(["Dataline", "PlayerLinenumber"], axis=1)

    y["similarity"] = scores
    if ignore_search_words == True:
        words = query.split()
        for word in words:
            y = y[~y["PlayerLine"].str.contains(word.lower(), case=False)]
    st.markdown(y.to_markdown(), unsafe_allow_html=True)
