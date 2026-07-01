# DataBot

DataBot is a command-line AI assistant focused on data science, machine learning, statistics, Python, SQL, data analytics, and related project workflows.

The bot uses the OpenAI API and a custom system prompt to provide structured, beginner-friendly responses for common data science tasks such as debugging code, explaining concepts, checking model performance, and generating data project code snippets.

## Features

- Data science focused assistant behavior
- Scope control for off-topic questions
- Conversation memory during a single terminal session
- Configurable OpenAI model using an environment variable
- Beginner-friendly command-line interface

## Project Files

```text
databot.py       Main DataBot application
test_api.py      Simple OpenAI API chatbot test script
requirements.txt Python package dependencies
README.md        Project documentation
```

## Requirements

- Python 3.10 or newer
- An OpenAI API key
- Git, if you want to upload the project to GitHub

## Setup

1. Clone or download this project.

2. Install the required package:

```powershell
pip install -r requirements.txt
```

3. Set your OpenAI API key.

For the current PowerShell session:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

To set it permanently on Windows:

```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

After using `setx`, close and reopen your terminal before running the bot.

## Usage

Run DataBot:

```powershell
python databot.py
```

Then type a prompt:

```text
You: Explain overfitting in machine learning.
```

To stop the bot:

```text
quit
```

or:

```text
exit
```

## Optional Model Configuration

By default, DataBot uses:

```text
gpt-4o
```

You can choose another model by setting `OPENAI_MODEL`:

```powershell
$env:OPENAI_MODEL="gpt-4o-mini"
python databot.py
```

## Example Prompts

```text
Explain precision, recall, and F1-score for fraud detection.
```

```text
Generate Python code to check missing values in a pandas DataFrame.
```

```text
My Random Forest model has 99% training accuracy but 61% test accuracy. What is happening?
```

## Notes

- Do not commit your API key to GitHub.
- Keep secrets in environment variables, not in Python files.
- DataBot is designed for learning and project support, not as a replacement for professional advice.

## License

No license has been selected yet. Add a license before sharing or accepting contributions publicly.
