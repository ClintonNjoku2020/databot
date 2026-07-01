# DataBot

DataBot is a command-line AI assistant designed to help with data science, data analytics, machine learning, statistics, Python, SQL, and related project workflows. It uses the OpenAI API with a custom system prompt so it can give structured, beginner-friendly answers for explanations, debugging, model evaluation, and data project code.

## Requirements

- Python 3.10 or newer
- An OpenAI API key
- Required Python libraries:

```powershell
pip install openai python-dotenv
```

You can also install the project requirements with:

```powershell
pip install -r requirements.txt
```

## Setup

1. Clone the repository:

```powershell
git clone https://github.com/ClintonNjoku2020/databot.git
cd databot
```

2. Create a `.env` file:

```powershell
copy .env.example .env
```

3. Add your OpenAI API key to `.env`:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o
```

The `.env` file is listed in `.gitignore`, so your real API key should stay on your computer and should not be pushed to GitHub.

4. Run DataBot:

```powershell
python databot.py
```

5. Type a prompt after `You:`. To stop the bot, type:

```text
quit
```

or:

```text
exit
```

## Example Conversations

### Example 1: Explaining a Machine Learning Concept

```text
You: Explain overfitting in machine learning with a simple example.

DataBot: Overfitting happens when a machine learning model learns the training data too closely, including noise, random patterns, or unusual examples.

A simple example:

Imagine you train a model to predict house prices. In the training data, one expensive house happens to have a red door. An overfitted model might learn:

red door = expensive house

But in real life, the red door is probably not the true reason the house is expensive. The model has learned a random pattern from the training data instead of the real relationship.

Key takeaway: overfitting means the model memorizes the training data instead of learning patterns that generalize to new data.
```

### Example 2: Diagnosing Model Performance

```text
You: My Random Forest model has 99% training accuracy but only 61% test accuracy. What is likely happening?

DataBot: Your Random Forest model is likely overfitting.

It has learned the training data very well, including noise or dataset-specific patterns, but those patterns do not generalize well to new unseen data.

Common causes:
1. The trees are too deep.
2. The model has too many complex splits.
3. There is noise or leakage in the training data.
4. The dataset is small.
5. The train and test sets come from different distributions.

Recommended fixes:
1. Limit tree depth using max_depth.
2. Increase min_samples_leaf or min_samples_split.
3. Use cross-validation.
4. Check for data leakage.
5. Remove noisy or irrelevant features.
```

### Example 3: Handling an Out-of-Scope Question

```text
You: What is Amen?

DataBot: I am DataBot, a specialist assistant for data science and machine learning, so I cannot answer that directly because it is outside my scope.

I can help with a related data science topic, such as analyzing religious text data, building an NLP keyword classifier, or cleaning text data for sentiment analysis.
```

## Prompt Engineering Techniques Used

### Chain-of-Thought Style Guidance

The system prompt tells DataBot to reason carefully and break complex data science problems into clear stages before giving an answer. In plain English, this means the bot is guided to think through the problem in an organized way instead of giving a rushed or vague response.

### Few-Shot Prompting

The system prompt includes example conversations for diagnosis, explanation, and code responses. These examples show the bot the style, structure, and level of detail expected, so future answers follow a similar pattern.

### System Prompt Design

The system prompt defines DataBot's role, behavior, scope, and output format. It tells the bot to focus on data science topics, avoid inventing facts, ask clarifying questions when needed, and use consistent response structures for explanations, diagnoses, and code.

## What I Would Improve

- Add better error handling for API failures, invalid API keys, network problems, and rate limits.
- Add automated tests so changes to the prompt or command-line flow can be checked more safely.
- Add a cleaner user interface, such as a simple web app or Streamlit app, so beginners can use DataBot without the command line.

## Notes

- Do not commit your real API key to GitHub.
- Keep secrets in `.env` or environment variables, not in Python files.
- Commit `.env.example`, but never commit `.env`.
