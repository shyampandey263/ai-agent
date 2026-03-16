from groq import Groq
from ddgs import DDGS
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("Ggsk_g5DIEDMb9CHha9DNXYivWGdyb3FYAQs3OzrXxczrl87yoV0XEPFI"))

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


# Run loop
while True:
    query = input("\nAsk Research Agent: ")

    if query.lower() == "exit":
        break

    answer = research_agent(query)

    print("\nResearch Summary:\n")
    print(answer)