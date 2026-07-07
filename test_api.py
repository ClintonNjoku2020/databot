from openai import OpenAIError

from databot import create_client, get_api_key, get_model


MAX_HISTORY_MESSAGES = 20


def main():
    api_key = get_api_key()
    if not api_key or api_key == "your_api_key_here":
        print("Missing OPENAI_API_KEY. Add your API key, then run this script again.")
        return

    client = create_client(api_key)
    model = get_model()

    messages = [
        {
            "role": "system",
            "content": "You are a helpful conversational AI assistant.",
        }
    ]

    print("Chatbot ready. Type 'exit' or 'quit' to stop.")

    while True:
        try:
            user_input = input("You: ").strip()
        except EOFError:
            break

        if user_input.lower() in {"exit", "quit"}:
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        if len(messages) > MAX_HISTORY_MESSAGES + 1:
            messages = [messages[0]] + messages[-MAX_HISTORY_MESSAGES:]

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
        except OpenAIError as error:
            messages.pop()
            print(f"Bot error: {error}")
            print("Check your API key, model name, internet connection, billing status, or rate limits, then try again.")
            continue
        except KeyboardInterrupt:
            print("\nChatbot stopped.")
            break

        assistant_message = response.choices[0].message.content or "I could not generate a response."
        print(f"Bot: {assistant_message}")

        messages.append({"role": "assistant", "content": assistant_message})


if __name__ == "__main__":
    main()
