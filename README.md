# AI Linkedin Profile Scraper

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LangChain](https://img.shields.io/badge/LangChain-🔗-orange)](https://python.langchain.com/)
[![Gemini API](https://img.shields.io/badge/Gemini%202.0-API-blueviolet)](https://ai.google.dev/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/linkedin-scraper-gemini/pulls)

This project is an **AI-powered LinkedIn profile scraper** that uses [Google Gemini 2.0](https://ai.google.dev/) (via LangChain) and a headless browser automation library ([`browser-use`](https://pypi.org/project/browser-use/)) to extract and cache LinkedIn profile information programmatically.

It automates the task of visiting LinkedIn connection pages, scraping profile names and URLs, and storing the data with caching and infinite loop protection.

---

## 🔍 Features

- 🚀 Automates LinkedIn browsing using `browser-use`
- 🧠 Uses `Gemini 2.0` for intelligent task reasoning (via `LangChain`)
- 🧾 Extracts up to 200 profile names and URLs from LinkedIn connections
- 💾 Caching system to avoid re-scraping the same profiles
- 🔄 Detects infinite loops in automation steps
- ✅ Typed output validation with `Pydantic`
- 🔐 Environment variable management with `.env`

---

## 📁 Output

- Scraped profiles are saved in:
  - `linkedin_profile_data.json` – latest session results
  - `profile_cache.json` – cumulative cache of visited profiles

Each profile follows this structure:

```json
{
  "profile_name": "John Doe",
  "profile_url": "https://www.linkedin.com/in/johndoe"
}
```

## 📦 Requirements
Python 3.8+

Google Chrome (pre-installed)

A valid Gemini API key

## 📚 Python Dependencies
Install via pip:

```bash
pip install -r requirements.txt
```
Or manually:
```bash
pip install langchain-google-genai browser-use python-dotenv pydantic
```
## ⚙️ Setup
1. Clone the repository
```bash
git clone https://github.com/harsh16629/AI-Linkedin-profile-scraper.git
cd linkedin-scraper-gemini
```
2. Create a .env file
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```
3. Update Chrome path
```bash
chrome_instance_path='[YOUR CHROME PATH]'
```
## 🧠 How It Works
- Uses a task-driven LLM agent to automate browsing in LinkedIn.
- Visits "My Network" page, opens the first profile, scrapes name + URL.
- Repeats for ~200 profiles or until the maximum step limit is hit.
- Avoids previously visited profiles using a JSON-based cache.
- Prevents infinite loops using a sliding history window (deque).

# ▶️ Usage
Run the script:
```bash
python main.py
```
The script will:

- Launch Chrome and navigate to LinkedIn (ensure you're logged in!)
- Start extracting profiles
- Save new data in linkedin_profile_data.json

## 📁 Output files
- linkedin_profile_data.json
  ``` json
  [
    {
        "profile_name": "Pratik Meshram",
        "profile_url": "https://www.linkedin.com/in/pratik-meshram-6b46974b"
    },
    {
        "profile_name": "Rajkiran Biradar",
        "profile_url": "https://www.linkedin.com/in/rajkiran-biradar-b8178582"
    },
  ]
  ```
- profile_cache.json
  ```json
  {
    "visited_urls": [
        "https://www.linkedin.com/in/pratik-meshram-6b46974b",
        "https://www.linkedin.com/in/rajkiran-biradar-b8178582",
    ]
  "profiles": [
        {
            "profile_name": "Pratik Meshram",
            "profile_url": "https://www.linkedin.com/in/pratik-meshram-6b46974b"
        },
        {
            "profile_name": "Rajkiran Biradar",
            "profile_url": "https://www.linkedin.com/in/rajkiran-biradar-b8178582"
        },
    ]
  }
  ```


## 📌 Notes
- Make sure you're logged into LinkedIn in the Chrome profile used by the script.
- The Gemini model used is gemini-2.0-flash-exp. You can change it to another variant in the script.
- Chrome must be installed locally and accessible via the provided path.

📄 File Structure
```bash
.
├── linkedin_scraper.py         # Main Python script
├── linkedin_profile_data.json  # Output: scraped profiles
├── profile_cache.json          # Output: cached profiles
├── .env                        # API keys and secrets
├── README.md                   # Project documentation
└── requirements.txt            # Dependencies (optional)
```
## 🔐 Disclaimer
This project is for educational and research purposes only. Automated scraping of LinkedIn may violate their Terms of Service. Use responsibly and ensure compliance with platform policies.

## 📜 License
This project is licensed under the [MIT License](LICENSE).
