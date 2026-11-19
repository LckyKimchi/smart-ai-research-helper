# smart-ai-research-helper

# 🔍 Autonomous AI Research Assistant

An agentic web application built with **Python**, **Streamlit**, and the **Google Gemini API**. Given any research prompt, the AI autonomously plans queries, searches the live web using DuckDuckGo, synthesizes information across multiple sources, and outputs a structured briefing with clickable citations.

## ✨ Key Features
* **Autonomous Tool Calling:** Uses Gemini's native function-calling capabilities to decide when and what to search on the web—performing multiple searches automatically if initial results aren't enough.
* **Live Web Grounding:** Integrates `ddgs` (DuckDuckGo Search) to pull real-time information, preventing outdated knowledge cutoffs.
* **Resilient Model Fallback:** Automatically cascades through backup Gemini models (`gemini-2.5-flash` → `gemini-2.5-flash-lite`) if a primary endpoint experiences high traffic (`503`) or unavailability (`404`).
* **Real-Time Status & Clean UI:** Displays live search progress indicators (`st.status`) and supports keyboard form submission via Streamlit.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Frontend:** [Streamlit](https://streamlit.io)
* **LLM & Agent Framework:** [Google GenAI SDK](https://google.dev) (`google-genai`)
* **Search Tool:** [DDGS](https://pypi.org) (DuckDuckGo Search)

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com
cd your-repo-name
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a Gemini API Key
1. Visit [Google AI Studio](https://google.com) and generate a free API key.
2. Either enter the key directly in the app's sidebar when running locally, or create `.streamlit/secrets.toml` with:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```

### 4. Run the app
```bash
streamlit run app.py
```

## 🧠 How It Works
1. **User Input:** The user submits a topic or comparison query through the Streamlit form.
2. **Agent Loop:** The prompt and the `search_web` Python function schema are passed to Gemini with a low temperature (`0.3`) to prioritize factual accuracy.
3. **Tool Execution:** Gemini invokes `search_web(query)` one or more times, parses the returned titles, URLs, and snippets, and synthesizes the final markdown report with inline links.
