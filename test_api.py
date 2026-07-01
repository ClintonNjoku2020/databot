import os

from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("Missing OPENAI_API_KEY. Add your API key to the local .env file, then run this script again.")
        return

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o")

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

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )

        assistant_message = response.choices[0].message.content
        print(f"Bot: {assistant_message}")

        messages.append({"role": "assistant", "content": assistant_message})


if __name__ == "__main__":
    main()
