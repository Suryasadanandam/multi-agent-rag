import os
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_agent(topic: str) -> str:
    print(f"Agent 1: Searching web for {topic}...")
    results = tavily_client.search(
        query=topic,
        max_results=5
    )
    search_data = ""
    for r in results["results"]:
        search_data += f"Title: {r['title']}\n"
        search_data += f"Content: {r['content']}\n"
        search_data += f"URL: {r['url']}\n\n"
    return search_data

def summarize_agent(search_data: str, topic: str) -> str:
    print("Agent 2: Summarizing search results...")
    prompt = f"""You are a research summarizer.
Summarize the following search results about "{topic}" 
into clear key points.

Search Results:
{search_data}

Give a structured summary with:
- Main findings
- Key statistics
- Important facts
"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content

def report_agent(summary: str, topic: str) -> str:
    print("Agent 3: Writing final report...")
    prompt = f"""You are a professional research report writer.
Write a detailed research report about "{topic}" 
using the following summary.

Summary:
{summary}

Write a professional report with these sections:
1. Introduction
2. Key Findings
3. Analysis
4. Conclusion
5. Sources Summary

Make it professional and detailed.
"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048
    )
    return response.choices[0].message.content