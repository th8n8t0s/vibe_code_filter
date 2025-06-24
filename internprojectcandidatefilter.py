import requests
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------- CONFIG -------- #
GITHUB_TOKEN = 'your_github_token_here'  # Optional for private repos or rate limit

# -------- HELPERS -------- #
def fetch_github_readme(repo_url):
    match = re.match(r"https://github.com/(.+)/(.+)", repo_url)
    if not match:
        return ""
    owner, repo = match.group(1), match.group(2)
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

# -------- MAIN FUNCTION -------- #
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

# -------- EXAMPLE USAGE -------- #
if __name__ == "__main__":
    candidates = [
        {'name': 'Alice', 'github': 'https://github.com/octocat/Hello-World', 'notion': 'https://www.notion.so/samplepage1'},
        {'name': 'Bob', 'github': 'https://github.com/torvalds/linux', 'notion': 'https://www.notion.so/samplepage2'},
    ]
    keywords = "creative coding p5.js generative art javascript interactive"

    ranked = evaluate_candidates(candidates, keywords)
    print(json.dumps(ranked, indent=2))

