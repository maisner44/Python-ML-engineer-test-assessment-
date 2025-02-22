import os
from dotenv import load_dotenv
from app.vector_db.faiss_integration import get_context_for_query

load_dotenv()

import openai


openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("No OpenAI API key found. Please set it in your .env file.")

def get_additional_context(query: str) -> str:
    # Retrieve relevant cocktail context from the vector DB
    context = get_context_for_query(query, k=5)
    return context

# Generate a response using OpenAI GPT with Retrieval Augmented Generation (RAG).
def generate_response(query: str) -> str:
    additional_context = get_additional_context(query)

    # Construct the prompt by merging the query with the additional context and set up a role of cocktail advisoe for model
    prompt = (
        f"You are a cocktail advisor with extensive knowledge about cocktail recipes, ingredients, "
        f"and user preferences. Use the following context to help answer the query.\n\n"
        f"Context: {additional_context}\n\n"
        f"Query: {query}\n\n"
        f"Answer:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable cocktail advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print("Error during OpenAI API call:", e)
        return "OpenAI API error"

if __name__ == "__main__":
    sample_query = "What are 5 cocktails containing lemon?"
    print("Query:", sample_query)
    print("Response:", generate_response(sample_query))
