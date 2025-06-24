#  Vibe Code Filter

A Streamlit-based tool that helps filter internship applicants by analyzing their GitHub and Notion submissions for relevance to a given set of “vibe” keywords — no resumes required.

##  Why This Exists

For creators, founders, or builders hiring via TikTok, Substack, or DMs, reviewing proof-of-work is hard to scale. This tool was designed to make that fast, fair, and automatic — starting with keyword relevance and expandable into full AI-assisted evaluation.

---

##  What It Does

-  **Accepts GitHub + Notion links** for each candidate
-  **Scrapes their content** using GitHub API and HTML parsing
-  **Ranks candidates** based on cosine similarity to your vibe keywords
-  **Displays live scores**, sorted by relevance
-  **Exports ranked candidates** in downloadable JSON format

---

##  How to Use

###  Local

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open [http://localhost:8501](http://localhost:8501)

###  Deploy Online

Use [https://streamlit.io/cloud](https://streamlit.io/cloud)  
- Link to this repo  
- Set main file as: `streamlit_app.py`

---

##  Features

- Add candidates one by one using a clean form
- See a running list of all added entries
- Filter and rank by custom keywords
- Download final scores in `.json` format

---

##  Future Plans

This is the manual-friendly MVP. Here's what can come next:

-  **Automated DM/email parsing:** Pull candidate info directly from TikTok DMs, email, or Discord using a pre-defined format
-  **Standardized intake schema:** Define a format like:
  ```
  Name | GitHub URL | Notion URL | Optional pitch
  ```
  Then automate extraction into a CSV or JSON for bulk import
-  **LLM-based scoring layer:** Use GPT/Claude to summarize vibe alignment and creativity, beyond keyword matching

---

##  Built With

- Python + Streamlit
- GitHub API
- BeautifulSoup (Notion scraper)
- scikit-learn (TF-IDF & cosine similarity)

---
## this is the live link for the demo - ### 🔗 Live Demo: [https://vibecodefilter.streamlit.app](https://vibecodefilter.streamlit.app)

##  Author

Built by Immanuel Garcia — designed to make human-first hiring faster and more intelligent.
