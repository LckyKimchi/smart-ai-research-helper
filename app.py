import streamlit as st
from google import genai
from google.genai import types
from ddgs import DDGS

# 1. Page Setup
st.set_page_config(page_title="Smart AI Research Helper", page_icon="🔍")
st.title("🔍 Autonomous Research Assistant")
st.write("Ask any question. The AI will search the live web, read sources, and write a cited briefing.")

# 2. Define the Web Search Tool
def search_web(query: str) -> str:
    """Searches the web using DuckDuckGo and returns the top results."""
    with st.status(f"🌐 Searching the web for: '{query}'...", expanded=False):
        try:
            results = DDGS().text(query, max_results=5)
            if not results:
                return "No results found."
            
            formatted_results = []
            for r in results:
                formatted_results.append(
                    f"Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}\n"
                )
            return "\n---\n".join(formatted_results)
        except Exception as e:
            return f"Search error: {str(e)}"

# 3. Get API Key (from Streamlit Secrets or User Input)
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else None
if not api_key:
    api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

# 4. Main App Interface
topic = st.text_input("What would you like me to research?", placeholder="e.g., Compare the latest MacBook Air vs Dell XPS 13")

if st.button("Research Topic", type="primary"):
    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar first.")
    elif not topic:
        st.warning("Please enter a research topic.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            You are an expert research assistant. Research the following topic thoroughly using your web search tool.
            You may perform multiple searches if needed to get complete, up-to-date facts.
            
            Topic: {topic}
            
            Instructions:
            - Synthesize the findings into a clear, well-structured briefing with bullet points.
            - Include clickable markdown links to your sources throughout the text or in a Sources section at the end.
            """

            with st.spinner("Agent is thinking and gathering sources..."):
                models_to_try = ["gemini-2.5-flash", "gemini-2.5-flash-lite"]
                response = None
                last_error = None

                for model_name in models_to_try:
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                tools=[search_web],
                                temperature=0.3,
                            ),
                        )
                        break
                    except Exception as model_err:
                        last_error = model_err
                        if "503" in str(model_err) or "404" in str(model_err):
                            continue
                        raise model_err

                if not response:
                    raise last_error
            
            st.markdown("### Research Briefing")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
