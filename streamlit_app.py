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
# App Setup
# ----------------------------

st.set_page_config(page_title="Vibe Code Filter", layout="wide")
st.title("Vibe Code Filter")

tab1, tab2 = st.tabs(["Submit & Score", "Dashboard View"])

# ----------------------------
# Session Storage
# ----------------------------

if "candidates" not in st.session_state:
    st.session_state["candidates"] = []

# ----------------------------
# TAB 1: Manual Submission + Re-ranking
# ----------------------------

with tab1:
    st.subheader("Manual Entry")

    with st.form("candidate_form"):
        name = st.text_input("Candidate Name")
        github_url = st.text_input("GitHub URL")
        notion_url = st.text_input("Notion URL")
        submitted = st.form_submit_button("Add Candidate")

    if submitted:
        github_text = fetch_github_readme(github_url)
        notion_text = fetch_notion_text(notion_url)
        combined_text = github_text + " " + notion_text
        st.session_state["candidates"].append({
            "Name": name,
            "GitHub": github_url,
            "Notion": notion_url,
            "Text": combined_text
        })

    st.markdown("### Keyword Filter")
    vibe_keywords = st.text_input("Enter keywords for scoring", value="automation ai fast")

    for candidate in st.session_state["candidates"]:
        candidate["Score"] = round(compute_score(candidate["Text"], vibe_keywords), 4)

    if st.session_state["candidates"]:
        df = pd.DataFrame(st.session_state["candidates"]).drop(columns=["Text"])
        df = df.sort_values(by="Score", ascending=False)

        st.markdown("### Ranked Candidates")
        st.dataframe(df, use_container_width=True)

        st.download_button("Download CSV", df.to_csv(index=False), file_name="ranked_candidates.csv")
        st.download_button("Download JSON", df.to_json(orient="records"), file_name="ranked_candidates.json")

        st.markdown("### Remove Candidate")
        names = [c["Name"] for c in st.session_state["candidates"]]
        name_to_delete = st.selectbox("Select a candidate to remove", [""] + names)
        if name_to_delete:
            st.session_state["candidates"] = [c for c in st.session_state["candidates"] if c["Name"] != name_to_delete]
            st.success(f"Deleted {name_to_delete}. Refresh view to update table.")

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
