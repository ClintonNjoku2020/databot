from types import SimpleNamespace

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
