# DataBot

DataBot is an AI assistant for data science, data analytics, machine learning, statistics, Python, SQL, and related project workflows. It is presented inside a responsive Streamlit portfolio with Home, About Me, DataBot, Projects, and Contact pages. The repository also includes a command-line interface. DataBot uses the OpenAI API with a custom system prompt so it can give structured, beginner-friendly answers for explanations, debugging, model evaluation, and data project code. In the Streamlit app, users can also generate downloadable PDFs, charts, workflow diagrams, and PowerPoint presentations from a brief or CSV-backed dataset.

To control API costs, DataBot uses a compact system prompt and rolling conversation
summaries. Recent messages remain unchanged, while older messages are periodically
compressed into a short context summary.

## Live Deployment

The portfolio and DataBot are deployed at:

```text
https://clintonnjoku.com
https://clintonnjoku.com/databot
```

The same app is also available through Streamlit Community Cloud:

```text
https://clinton-data-ai-portfolio.streamlit.app
https://clinton-data-ai-portfolio.streamlit.app/databot
```

The custom domain is served from an Ubuntu VPS. The Streamlit app runs locally on the server at `127.0.0.1:8501`, and the public domain forwards web traffic to that local Streamlit process through the server's web/proxy configuration.

DataBot supports file uploads directly in the chat input. Users can attach CSV and text-based files, then ask questions about the uploaded data. DataBot can also fetch readable text from public web pages supplied by URL and use those sources for clear market research with citations. The `Create files` tab generates professional report artifacts locally in the app:

- PDF report
- SVG chart
- SVG workflow diagram
- PowerPoint presentation

CSV uploads in the artifact generator are used to infer chart labels and numeric values.

## Internet Market Research

Open the DataBot page, then expand `Internet market research` in the Chat tab.

1. Select `Fetch internet sources for this question`.
2. Paste up to five public source URLs, one per line.
3. Ask a market research question, such as:

```text
Compare the positioning, customer signals, risks, and next steps for this market.
```

DataBot fetches the page text, passes the extracted source context into the model, and instructs the model to separate sourced facts from interpretation. Factual web claims should cite source numbers such as `[S1]` and DataBot should state when the sources are too thin to support a conclusion.

You can also paste URLs directly into the chat message. DataBot will use them as source context for that question.

## Requirements

- Python 3.11 or newer
- An OpenAI API key
- Required Python libraries:

```powershell
pip install -r requirements.txt
```

If `pip` is not recognized on Windows, use:

```powershell
python -m pip install -r requirements.txt
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
OPENAI_MODEL=gpt-4o-mini
```

The `.env` file is listed in `.gitignore`, so your real API key should stay on your computer and should not be pushed to GitHub.

4. For the Streamlit web app, you can also create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your_api_key_here"
OPENAI_MODEL = "gpt-4o-mini"
```

The `.streamlit/secrets.toml` file is listed in `.gitignore`, so your real API key should not be pushed to GitHub.

5. Run the web app:

```powershell
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

6. Or run DataBot in the terminal:

```powershell
python databot.py
```

7. Type a prompt after `You:`. To stop the bot, type:

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

Confidence: 5/5
```

## Generating Files

Open the DataBot page, then select the `Create files` tab.

1. Enter a title for the report or presentation.
2. Add a short brief describing the audience, objective, and desired output.
3. Add key points, one per line.
4. Optionally upload a CSV file so DataBot can infer chart data from the first usable numeric column.
5. Click `Generate files`.
6. Download the PDF, chart, diagram, or PowerPoint file.

The artifact generator runs locally in the Streamlit app. It does not require the OpenAI API to create the files, although the chat assistant can still help users write better briefs, analysis summaries, slide outlines, chart descriptions, and diagram steps.

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

Confidence: 5/5
```

### Example 3: Handling an Out-of-Scope Question

```text
You: What is Amen?

DataBot: I am DataBot, a specialist assistant for data science and machine learning, so I cannot answer that directly because it is outside my scope.

I can help with a related data science topic, such as analyzing religious text data, building an NLP keyword classifier, or cleaning text data for sentiment analysis.

Confidence: 5/5
```

## Prompt Engineering Techniques Used

### Chain-of-Thought Style Guidance

The system prompt tells DataBot to reason carefully and break complex data science problems into clear stages before giving an answer. In plain English, this means the bot is guided to think through the problem in an organized way instead of giving a rushed or vague response.

### Few-Shot Prompting

The system prompt includes example conversations for diagnosis, explanation, and code responses. These examples show the bot the style, structure, and level of detail expected, so future answers follow a similar pattern.

### System Prompt Design

The system prompt defines DataBot's role, behavior, scope, and output format. It tells the bot to focus on data science topics, avoid inventing facts, ask clarifying questions when needed, and use consistent response structures for explanations, diagnoses, and code.

## What I Would Improve

- Add conversation export so users can save useful answers from a terminal session.
- Add token-usage reporting so deployment costs can be monitored in the interface.

## Testing DataBot Manually

Run the chatbot:

```powershell
python databot.py
```

Or run the Streamlit app:

```powershell
streamlit run app.py
```

Then try these prompts:

```text
Explain overfitting in machine learning with a simple example.
```

```text
My model accuracy is stuck at 62%. What should I check?
```

```text
What is Amen?
```

Expected behavior:

- Data science questions should receive structured, beginner-friendly answers.
- Diagnosis-style questions should use numbered sections.
- Clearly out-of-scope questions should be redirected to a related data science topic.
- Every answer should end with a confidence score from 1 to 5.

## Deploying on Streamlit Community Cloud

1. Make sure the latest code is pushed to GitHub.

2. Go to:

```text
https://share.streamlit.io
```

3. Click `Create app`.

4. Select:

```text
Repository: ClintonNjoku2020/databot
Branch: main
Main file path: app.py
```

5. Open `Advanced settings`.

6. Set the Python version to `3.12` or any supported Python version newer than `3.11`.

7. In the `Secrets` field, paste:

```toml
OPENAI_API_KEY = "your_real_api_key_here"
OPENAI_MODEL = "gpt-4o-mini"
```

8. Click `Save`, then click `Deploy`.

Do not commit `.streamlit/secrets.toml` or your real API key to GitHub. Streamlit Community Cloud stores deployment secrets separately from your repository.

## Current VPS Deployment

The custom domain deployment uses an Ubuntu VPS with the repository checked out at:

```bash
/root/databot
```

The app runs inside the project virtual environment:

```bash
/root/databot/.venv
```

The Streamlit process is started with:

```bash
/root/databot/.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

The app is bound to `127.0.0.1` so it is not exposed directly on the public internet. The public site at `https://clintonnjoku.com` reaches the app through the VPS web/proxy layer, which forwards requests to `127.0.0.1:8501`.

To update the VPS deployment after pushing changes to GitHub:

```bash
cd /root/databot
git pull
/root/databot/.venv/bin/pip install -r requirements.txt
kill $(pgrep -f "streamlit run app.py")
nohup /root/databot/.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501 > /root/databot/streamlit.log 2> /root/databot/streamlit.err.log &
```

To confirm the Streamlit process is running:

```bash
ps aux | grep streamlit
```

Expected process:

```text
/root/databot/.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Logs are written to:

```text
/root/databot/streamlit.log
/root/databot/streamlit.err.log
```

## Troubleshooting

- If you see `Missing OPENAI_API_KEY`, check that `.env` exists and contains your real API key.
- If OpenAI rejects your API key, create or copy a valid API key from your OpenAI Platform project.
- If OpenAI says the key has no available quota, check billing, credits, and project limits in your OpenAI Platform account.
- If you see an API error, check your API key, model name, internet connection, billing status, and rate limits.
- If the model name does not work for your account, update `OPENAI_MODEL` in `.env` and `.env.example`.
- If `clintonnjoku.com` does not show the latest GitHub changes but the `.streamlit.app` URL does, SSH into the VPS, run `git pull` in `/root/databot`, and restart the local Streamlit process.

## Notes

- Do not commit your real API key to GitHub.
- Keep secrets in `.env` or environment variables, not in Python files.
- For Streamlit, keep secrets in `.streamlit/secrets.toml`.
- Commit `.env.example` and `.streamlit/config.toml`, but never commit `.env` or `.streamlit/secrets.toml`.
