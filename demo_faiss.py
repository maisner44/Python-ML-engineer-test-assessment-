from app.vector_db.faiss_integration import get_context_for_query, store_user_memory

def main():
    query = "I want cocktails with lemon and mint"
    context = get_context_for_query(query, k=3)
    print("Retrieved context:\n", context)

    store_user_memory("I love using fresh basil and elderflower in my cocktails.")

    new_context = get_context_for_query("Tell me about cocktails with basil", k=3)
    print("New context after storing user memory:\n", new_context)

if __name__ == "__main__":
    main()
