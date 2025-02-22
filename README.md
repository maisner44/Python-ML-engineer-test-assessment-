# Python-ML-engineer-test-assessment-

# Cocktail Advisor Chat

Cocktail Advisor Chat is a Python-based chat application that uses Retrieval-Augmented Generation (RAG) to provide cocktail recommendations and answer cocktail-related queries. The system integrates OpenAI's GPT for natural language processing and FAISS as a vector database to store and retrieve cocktail data as well as user memories (favorite ingredients/cocktails).

## Project Overview

This project demonstrates how to:
- Build a REST API using FastAPI.
- Integrate OpenAI GPT with FAISS for Retrieval-Augmented Generation.
- Serve a chat interface (HTML, CSS, and JavaScript) via FastAPI.
- Automatically detect and store user preferences for personalized recommendations.

Description of the main endpoints in the project:

/query:
Accepts POST requests with a user question. It retrieves relevant cocktail data and user memories from the FAISS vector database, combines this context with the query, and generates a response using OpenAI GPT.

/memory:
Accepts POST requests with user-provided favorite ingredients or cocktails, storing this information in the FAISS vector database for future personalized

## The version of openai is 0.28.0

## Setup Instructions

### 1. Clone the Repository and Configure Environment Variables

OPENAI_API_KEY=your_openai_api_key_here

### 2. Run demo_fails.py
Optional step thta shows how we store data into faiss

### 3. Run the FastAPI Server
uvicorn main:app --reload

### 4. Access the Chat Interface
localhost/chat/index.html

#### How It Works
User Query and Memory Detection:

When a user submits a query, the system checks if the message contains phrases indicating favorite ingredients or cocktails.
If detected, the user memory is stored in the FAISS vector database for future personalized recommendations.
Retrieval-Augmented Generation (RAG):

The query is converted into an embedding, and FAISS retrieves the most relevant cocktail information and any stored user memories.
The retrieved context is combined with the original query to form an enriched prompt.
Response Generation:

The enriched prompt is sent to OpenAI's GPT model via the ChatCompletion API.
The generated response is returned to the chat interface and displayed to the user.

#### User Interface:

The chat interface is built with HTML, styled with CSS, and the interactions are managed by JavaScript.
A loading animation appears in place of the advisor's answer while the system processes the query.


#### Additional Features
User Memory Storage:
The system automatically stores user messages that indicate favorite ingredients or cocktails, so future responses can be more personalized.

Missing API Key:
Ensure the .env file is correctly configured with your OpenAI API key.

Network Issues:
Check any firewall or proxy settings if API calls fail.

##Example of use:
![image](https://github.com/user-attachments/assets/f215dcc9-b8bf-44b3-b447-22d4a01ab342)


