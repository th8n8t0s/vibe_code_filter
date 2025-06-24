import streamlit as st
import requests
import re
import json
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# GitHub token (optional)
GITHUB_TOKEN = ''  # Leave blank unless you hit rate limits

# --------- FUNCTIONS --------- #
def fetch_github_readme(repo_url):
    match = re.match(r"https://github.com/([\w\-]+)/([\w\-]+)", repo_url)
    if not match:
        return ""
    owner, repo = match.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    resp = requests.get(api_url, headers=headers)
    return resp.text if resp.status_code == 200 else ""

def fetch_notion_text(notion_url):
    try:
        resp = requests.get(notion_url, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code != 200:
            return ""
        soup = BeautifulSoup(resp.text, 'html.parser')
        return ' '.join([tag.get_text() for tag in soup.find_all(['p', 'h1', 'h2', 'h3'])])
    except:
        return ""

def score_against_keywords(texts, keywords):
    documents = texts + [keywords]
    tfidf = TfidfVectorizer().fit_transform(documents)
    cosine_sim = cosine_similarity(tfidf[-1], tfidf[:-1])
    return cosine_sim.flatten()

def evaluate_candidates(candidates, keywords):
    corpus = []
    for c in candidates:
        gh_text = fetch_github_readme(c['github']) if 'github' in c else ""
        notion_text = fetch_notion_text(c['notion']) if 'notion' in c else ""
        full_text = f"{gh_text}\n{notion_text}"
        corpus.append(full_text)

    scores = score_against_keywords(corpus, keywords)
    results = []
    for i, c in enumerate(candidates):
        results.append({
            'name': c.get('name', f'Candidate_{i+1}'),
            'score': round(float(scores[i]), 3),
            'github': c.get('github'),
            'notion': c.get('notion')
        })

    return sorted(results, key=lambda x: x['score'], reverse=True)

# --------- STREAMLIT UI --------- #
st.title("🔍 Vibe Code Filter Tool")
st.write("Evaluate candidates based on GitHub + Notion content relevance to your vibe.")

if 'candidates' not in st.session_state:
    st.session_state.candidates = []

keywords = st.text_input("🔑 Enter vibe keywords (comma-separated):", "creative coding, p5.js, generative art")

with st.form("add_candidate"):
    st.write("### Add a Candidate")
    name = st.text_input("Name")
    github = st.text_input("GitHub Repo URL")
    notion = st.text_input("Notion Page URL")
    submitted = st.form_submit_button("Add Candidate")
    if submitted:
        st.session_state.candidates.append({'name': name, 'github': github, 'notion': notion})
        st.success(f"Added {name}")

if st.session_state.candidates:
    st.write("### Current Candidates:")
    for idx, c in enumerate(st.session_state.candidates):
        st.markdown(f"**{idx+1}. {c['name']}**  ")
        st.markdown(f"GitHub: {c['github']}  ")
        st.markdown(f"Notion: {c['notion']}")
        st.markdown("---")

    if st.button("Run Filter"):
        results = evaluate_candidates(st.session_state.candidates, keywords)
        st.write("### Ranked Results:")
        for r in results:
            st.markdown(f"**{r['name']}** — Score: `{r['score']}`")
            st.markdown(f"- GitHub: {r['github']}")
            st.markdown(f"- Notion: {r['notion']}")
            st.markdown("---")

        # Optional CSV download
        json_results = json.dumps(results)
        st.download_button("Download Results (JSON)", json_results, file_name="ranked_candidates.json")
else:
    st.info("No candidates added yet. Use the form above to begin.")
