from types import SimpleNamespace

import httpx
from openai import OpenAIError

import databot


def response_with(content):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
    )


class FakeCompletions:
    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        result = self.results.pop(0)
        if isinstance(result, Exception):
            raise result
        return response_with(result)


def fake_client(*results):
    completions = FakeCompletions(results)
    client = SimpleNamespace(
        chat=SimpleNamespace(completions=completions)
    )
    return client, completions


def long_history():
    history = databot.create_conversation_history()
    for index in range(databot.SUMMARIZE_AFTER_MESSAGES):
        role = "user" if index % 2 == 0 else "assistant"
        history.append({"role": role, "content": f"message {index}"})
    return history


def test_system_prompt_is_compact():
    assert len(databot.SYSTEM_PROMPT) < 2_000


def test_short_conversation_uses_one_completion():
    client, completions = fake_client("A concise answer.")

    answer, history = databot.get_databot_reply(
        client=client,
        model="test-model",
        conversation_history=databot.create_conversation_history(),
        user_input="What is cross-validation?",
    )

    assert answer == "A concise answer."
    assert len(completions.calls) == 1
    assert history[-1] == {"role": "assistant", "content": answer}


def test_long_conversation_is_summarized_and_keeps_recent_messages():
    client, completions = fake_client("Important earlier context.", "Final answer.")

    answer, history = databot.get_databot_reply(
        client=client,
        model="test-model",
        conversation_history=long_history(),
        user_input="new question",
    )

    assert answer == "Final answer."
    assert len(completions.calls) == 2
    assert history[1]["content"] == (
        databot.SUMMARY_PREFIX + "Important earlier context."
    )
    assert history[-2] == {"role": "user", "content": "new question"}
    assert history[-1] == {"role": "assistant", "content": "Final answer."}
    assert len(history) == databot.RECENT_MESSAGES_TO_KEEP + 3

    main_request = completions.calls[1]["messages"]
    assert main_request[1]["content"].startswith(databot.SUMMARY_PREFIX)


def test_summary_failure_uses_local_fallback():
    client, completions = fake_client(OpenAIError("summary failed"), "Final answer.")

    answer, history = databot.get_databot_reply(
        client=client,
        model="test-model",
        conversation_history=long_history(),
        user_input="new question",
    )

    assert answer == "Final answer."
    assert len(completions.calls) == 2
    assert history[1]["content"].startswith(databot.SUMMARY_PREFIX)
    assert "message" in history[1]["content"]


def test_uploaded_csv_is_summarized_with_columns_and_sample_rows():
    uploaded_file = SimpleNamespace(
        name="sales.csv",
        type="text/csv",
        getvalue=lambda: b"region,sales\nNorth,10\nSouth,20\n",
    )

    summary = databot.summarize_uploaded_file(uploaded_file)

    assert "File: sales.csv" in summary
    assert "Columns (2): region, sales" in summary
    assert "sales: numeric" in summary
    assert "North,10" in summary


def test_user_input_with_files_includes_upload_context():
    uploaded_file = SimpleNamespace(
        name="notes.txt",
        type="text/plain",
        getvalue=lambda: b"Check missing values before modelling.",
    )

    prompt = databot.build_user_input_with_files("What should I do next?", [uploaded_file])

    assert "What should I do next?" in prompt
    assert "Uploaded file context follows" in prompt
    assert "Check missing values before modelling." in prompt


def test_user_input_with_saved_file_context_reuses_existing_upload():
    prompt = databot.build_user_input_with_file_context(
        "Which columns are numeric?",
        "File: sales.csv\nColumns (2): region, sales",
    )

    assert "Which columns are numeric?" in prompt
    assert "Uploaded file context follows" in prompt
    assert "File: sales.csv" in prompt


def test_extract_urls_deduplicates_and_trims_punctuation():
    urls = databot.extract_urls(
        "Compare https://example.com/report, and https://example.com/report against https://market.test/a."
    )

    assert urls == ["https://example.com/report", "https://market.test/a"]


def test_fetch_web_source_extracts_readable_html_with_mock_client():
    def handler(request):
        return httpx.Response(
            200,
            headers={"content-type": "text/html; charset=utf-8"},
            text=(
                "<html><head><title>Market Report</title><style>.x{}</style></head>"
                "<body><h1>Cloud analytics market</h1><script>ignore()</script>"
                "<p>Buyers want easier reporting and transparent pricing.</p></body></html>"
            ),
            request=request,
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))

    source = databot.fetch_web_source("https://example.com/report", client=client)

    assert source["error"] is None
    assert source["title"] == "Market Report"
    assert "Cloud analytics market" in source["text"]
    assert "transparent pricing" in source["text"]
    assert "ignore()" not in source["text"]


def test_web_research_context_and_prompt_require_citations():
    sources = [
        {
            "url": "https://example.com/report",
            "final_url": "https://example.com/report",
            "title": "Market Report",
            "content_type": "text/html",
            "fetched_at": "2026-07-20 10:00 UTC",
            "text": "Customers compare pricing, support, and setup time.",
            "error": None,
        }
    ]

    context = databot.format_web_research_context(sources)
    prompt = databot.build_user_input_with_web_context(
        "Research this market.",
        context,
    )

    assert "[S1] Market Report" in prompt
    assert "Cite source numbers like [S1]" in prompt
    assert "Sources used" in prompt
    assert "Sourced facts" in prompt
    assert "Recommendations" in prompt
    assert "Do not invent market size, revenue" in prompt
    assert "only when the source context states them" in prompt
    assert "weak, unavailable, thin, or outdated sources" in prompt


def test_source_references_markdown_lists_successful_and_unavailable_sources():
    references = databot.source_references_markdown(
        [
            {
                "title": "Market Report",
                "final_url": "https://example.com/report",
                "url": "https://example.com/report",
                "error": None,
            },
            {
                "title": "Blocked",
                "url": "https://example.com/blocked",
                "error": "403 Forbidden",
            },
        ]
    )

    assert "[S1] Market Report: https://example.com/report" in references
    assert "Sources unavailable:" in references
    assert "[S2] https://example.com/blocked: 403 Forbidden" in references


def test_unavailable_sources_markdown_lists_failed_sources_only():
    references = databot.unavailable_sources_markdown(
        [
            {
                "title": "Market Report",
                "final_url": "https://example.com/report",
                "url": "https://example.com/report",
                "error": None,
            },
            {
                "url": "https://example.com/blocked",
                "error": "403 Forbidden",
            },
        ]
    )

    assert references == "Sources unavailable:\n[S2] https://example.com/blocked: 403 Forbidden"
