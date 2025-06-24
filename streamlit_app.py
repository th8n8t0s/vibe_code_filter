import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------
# Utility Functions
# ----------------------------

def fetch_github_readme(github_url):
    try:
        username, repo = github_url.strip("/").split("/")[-2:]
        api_url = f"https://api.github.com/repos/{username}/{repo}/readme"
        headers = {"Accept": "application/vnd.github.v3.raw"}
        res = requests.get(api_url, headers=headers)
        return res.text if res.status_code == 200 else ""
    except:
        return ""

def fetch_notion_text(notion_url):
    try:
        res = requests.get(notion_url)
        soup = BeautifulSoup(res.text, "html.parser")
        return " ".join([p.text for p in soup.find_all(["p", "h1", "h2", "h3"])])
    except:
        return ""

def compute_score(candidate_text, keywords):
    texts = [candidate_text, keywords]
    tfidf = TfidfVectorizer().fit_transform(texts)
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

# ----------------------------
# App
# ----------------------------

st.set_page_config(page_title="Vibe Code Filter", layout="wide")
st.title("Vibe Code Filter")

tab1, tab2 = st.tabs(["Submit & Score", "Dashboard View"])

# ----------------------------
# TAB 1: Manual Submission + Scoring
# ----------------------------

with tab1:
    st.subheader("Manual Entry")

    with st.form("candidate_form"):
        name = st.text_input("Candidate Name")
        github_url = st.text_input("GitHub URL")
        notion_url = st.text_input("Notion URL")
        keywords = st.text_area("Vibe Keywords (comma or space-separated)")
        submitted = st.form_submit_button("Add Candidate")

    if "candidates" not in st.session_state:
        st.session_state["candidates"] = []

    if submitted:
        github_text = fetch_github_readme(github_url)
        notion_text = fetch_notion_text(notion_url)
        combined_text = github_text + " " + notion_text
        score = compute_score(combined_text, keywords)
        st.session_state["candidates"].append({
            "Name": name,
            "GitHub": github_url,
            "Notion": notion_url,
            "Score": round(score, 4)
        })

    if st.session_state["candidates"]:
        df = pd.DataFrame(st.session_state["candidates"])
        df = df.sort_values(by="Score", ascending=False)
        st.subheader("Ranked Candidates")
        st.dataframe(df, use_container_width=True)
        st.download_button("Download CSV", df.to_csv(index=False), file_name="ranked_candidates.csv")
        st.download_button("Download JSON", df.to_json(orient="records"), file_name="ranked_candidates.json")

# ----------------------------
# TAB 2: Dashboard Viewer
# ----------------------------

with tab2:
    st.subheader("Upload Ranked Candidates (CSV)")

    uploaded_file = st.file_uploader("Upload CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "Score" in df.columns:
            df = df.sort_values(by="Score", ascending=False)
        st.dataframe(df, use_container_width=True)
        st.download_button("Download CSV", df.to_csv(index=False), file_name="dashboard_ranking.csv")
