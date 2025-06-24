# Vibe Code Filter

A Streamlit-based tool that filters internship applicants by analyzing their GitHub and Notion submissions against user-defined keywords — no resumes required.

## Why This Exists

For creators or founders hiring from platforms like TikTok or Substack, reviewing proof-of-work from GitHub and Notion is hard to scale. This tool automates early filtering to help surface high-signal applicants without wasting hours manually opening tabs.

## What It Does

- Accepts GitHub + Notion links for each candidate
- Scrapes content from their README and Notion pages
- Ranks candidates using cosine similarity to a custom keyword list
- Displays sortable, downloadable results
- Offers a second tab for reviewing externally uploaded CSVs

## How to Use

### Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then go to: `http://localhost:8501`

### Deploy Online

Use [https://streamlit.io/cloud](https://streamlit.io/cloud)
- Link this repo
- Set main file: `streamlit_app.py`

## Features

- Manual form for entering candidate name + GitHub + Notion
- Keyword input box dynamically re-ranks candidates live
- Score is based on TF-IDF cosine similarity
- Option to delete candidates from view
- Upload existing CSV of ranked candidates (dashboard mode)
- Export results as `.csv` or `.json`

## Scaling Plans

If application volume increases significantly, the tool can be extended in the following ways:

### Option A: CSV Automation
- Accept a Google Form or Typeform using a defined schema:
  ```
  Name | GitHub URL | Notion URL | Optional pitch
  ```
- Automatically convert responses to CSV and process in batch

### Option B: Upgrade to Persistent Backend
- Store submissions in Airtable, Firebase, or Supabase
- Use scheduled backend function to:
  - Fetch and score new entries
  - Push live updates to a dashboard or export link

The app is structured to support either path with minimal change.

## Built With

- Python + Streamlit
- GitHub REST API
- BeautifulSoup for Notion scraping
- scikit-learn for keyword relevance scoring

## Author

Immanuel Garcia
