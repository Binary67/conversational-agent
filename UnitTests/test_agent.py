from __future__ import annotations

import pytest

from Agent import Agent


class DummyResult:
    def __init__(self, output: str) -> None:
        self.final_output = output


def test_agent_pipeline_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    blog_agent = Agent()

    call_order: list[str] = []

    def fake_run_sync(agent, input_text):
        call_order.append(agent.name)
        if agent.name == "Outline Writer":
            return DummyResult("Outline")
        if agent.name == "Content Writer" and len(call_order) == 2:
            return DummyResult("Draft content")
        if agent.name == "Proofread Writer":
            return DummyResult("Fix typos")
        return DummyResult("Corrected content")

    monkeypatch.setattr("agents.Runner.run_sync", fake_run_sync)
    monkeypatch.setattr("agents.set_default_openai_client", lambda *args, **kwargs: None)

    result = blog_agent.run("Some Title")
    assert result == "Corrected content"
    assert call_order == [
        "Outline Writer",
        "Content Writer",
        "Proofread Writer",
        "Content Writer",
    ]
