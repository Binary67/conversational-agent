from __future__ import annotations

import asyncio

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Agent import AgentCoordinator
from main import configure_logging


async def generate() -> str:
    coordinator = AgentCoordinator()
    return await coordinator.generate_blog("Test Title")


def test_generate_blog_runs() -> None:
    result = asyncio.run(generate())
    assert isinstance(result, str)
    assert len(result) > 0


def test_logging_file_created() -> None:
    log_path = "Logs/agents.log"
    if os.path.exists(log_path):
        os.remove(log_path)
    configure_logging()
    assert os.path.exists(log_path)


def test_output_file_written() -> None:
    output_path = "Logs/agents_output.txt"
    if os.path.exists(output_path):
        os.remove(output_path)
    asyncio.run(generate())
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as file:
        content = file.read()
    assert "Output from" in content
