# Vibe Code Filter

A Streamlit-based tool that filters internship candidates by analyzing their GitHub and Notion content for relevance to a custom set of keywords. Designed to support modern, proof-of-work-driven hiring—especially for roles where resumes aren’t the point.

---

## Why This Exists

This tool was built to help scale the review process for internships or freelance roles where applicants are submitting GitHub and Notion links instead of resumes. It allows you to prioritize quality submissions and filter through noise quickly.

---

## What It Does

- Accepts candidate info (Name, GitHub URL, Notion URL)
- Scrapes and parses GitHub READMEs and Notion pages
- Scores submissions using TF-IDF + cosine similarity against keyword prompts
- Ranks candidates by relevance and displays live results
- Exports results as CSV and JSON for downstream workflows

---

## Demo

Watch the full walkthrough:  
[Insert Loom link here]

Live app: [https://vibecodefilter.streamlit.app](https://vibecodefilter.streamlit.app)

---

## How to Use

### Online Deployment

Deployed via Streamlit Cloud. You can fork or clone this repo and deploy your own copy by setting the main file to `streamlit_app.py`.

---

### Input Methods

#### Manual Entry
Add candidates one at a time through the web interface.

#### CSV Upload
Upload a file with the following format:

```csv
Candidate Name,GitHub URL,Notion URL
```

This allows batch importing of submissions from sources like Google Forms or Sheets.

---

### Output

After processing, download ranked candidate data as either:
- CSV for spreadsheet analysis
- JSON for integration into other tools

---

## Scaling Considerations

The app is optimized for small to medium batches (50–100 candidates per session). To scale for higher volumes, you could:
- Route candidate intake via Google Forms → Sheets → CSV export
- Split sessions across multiple Streamlit deployments
- Add persistent intake using Firebase or Airtable
- Extend with LLM evaluation for creativity or alignment beyond keywords

---

## Built With

- Python
- Streamlit
- GitHub API
- BeautifulSoup (Notion scraping)
- scikit-learn (TF-IDF and cosine similarity)

---

## Author

Immanuel Garcia
