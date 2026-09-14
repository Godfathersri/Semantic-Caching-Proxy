# Semantic Caching Proxy for LLM APIs

A privacy-aware semantic caching middleware for LLM applications built with FastAPI, Gemini embeddings, and Qdrant.

## Problem

LLM applications often receive different prompts that are semantically asking the same question.

Traditional caching usually relies on exact text matching, so prompts such as:

- "What is machine learning?"
- "Can you explain machine learning?"
- "What does ML mean?"

may all trigger separate LLM API calls even though they require very similar answers.

This increases:
- API cost
- token usage
- response latency
- repeated computation

The goal of this project is to reuse previously generated responses when a new prompt is semantically similar to an existing one.

## What I Built

The application acts as a middleware layer between the client and the LLM provider.

When a prompt is submitted:

1. The request is received through a FastAPI endpoint.
2. Sensitive information is checked before caching.
3. An embedding is generated for the prompt.
4. The embedding is compared against previously stored prompts in Qdrant.
5. If a sufficiently similar prompt is found, the stored response is returned as a cache hit.
6. If no suitable match is found, the request is sent to the LLM provider.
7. The new prompt, embedding, and response are stored for future reuse.

## Architecture

Client  
↓  
FastAPI API  
↓  
PII Check  
↓  
Embedding Service  
↓  
Qdrant Vector Search  
↓  
Cache Decision  
├── Cache Hit → Return stored response  
└── Cache Miss → Call LLM → Store response → Return result

## Tech Stack

- Python
- FastAPI
- Gemini API
- Gemini Embeddings
- Qdrant
- Microsoft Presidio
- Docker
- Pydantic
- Git / GitHub

## Project Structure

```text
app/
├── main.py
├── config.py
├── schemas.py
├── routes/
│   ├── health.py
│   └── generate.py
├── services/
│   ├── llm_service.py
│   ├── embedding_service.py
│   ├── vector_store.py
│   └── cache_service.py
tests/
.env.example
requirements.txt
docker-compose.yml
