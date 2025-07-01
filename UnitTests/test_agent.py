from __future__ import annotations

import asyncio

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Agent import AgentCoordinator


async def generate() -> str:
    coordinator = AgentCoordinator()
    return await coordinator.generate_blog("Test Title")


def test_generate_blog_runs() -> None:
    result = asyncio.run(generate())
    assert isinstance(result, str)
    assert len(result) > 0
