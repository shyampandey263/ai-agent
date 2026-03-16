from fastapi import FastAPI
from groq import Groq
from ddgs import DDGS
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Home Page
@app.get("/")
def home():
    return {"message": "AI Agent API is running"}


# Web Search
def search_web(query):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(r["body"])
    return "\n".join(results)


# Research Agent
def research_agent(question):

    search_results = search_web(question)

    prompt = f"""
You are a research assistant.

Research topic:
{question}

Search results:
{search_results}

Write a clear research summary.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


# API Endpoint
@app.get("/research")
def get_research(query: str):

    answer = research_agent(query)

    return {
        "question": query,
        "research_summary": answer
    }