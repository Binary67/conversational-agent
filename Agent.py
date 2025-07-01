from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from logging.handlers import RotatingFileHandler
from pathlib import Path

from agents import Agent as OpenAiAgent, Runner, set_default_openai_client
from openai import AsyncAzureOpenAI


LOG_PATH = Path("Logs/agent.log")
LOG_PATH.parent.mkdir(exist_ok=True)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
if not _logger.handlers:
    handler = RotatingFileHandler(LOG_PATH, maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)
    _logger.addHandler(handler)


@dataclass
class Agent:
    """Coordinates multiple OpenAI agents to generate and proofread a blog."""

    outline_agent: OpenAiAgent = field(init=False)
    content_agent: OpenAiAgent = field(init=False)
    proofread_agent: OpenAiAgent = field(init=False)

    def __post_init__(self) -> None:
        if "OPENAI_API_VERSION" not in os.environ and "AZURE_OPENAI_API_VERSION" in os.environ:
            os.environ["OPENAI_API_VERSION"] = os.environ["AZURE_OPENAI_API_VERSION"]

        set_default_openai_client(AsyncAzureOpenAI())

        self.outline_agent = OpenAiAgent(
            name="Outline Writer",
            instructions=(
                "Create a concise outline with headings and bullet points for the given blog title."
            ),
        )

        self.content_agent = OpenAiAgent(
            name="Content Writer",
            instructions=(
                "Expand the outline into a full Markdown blog post. If corrections are provided, apply them."
            ),
        )

        self.proofread_agent = OpenAiAgent(
            name="Proofread Writer",
            instructions=(
                "Review the blog content and return a numbered list of corrections to make."
            ),
        )

    def run(self, title: str) -> str:
        """Generate and proofread content for ``title``."""

        _logger.info("Generating outline")
        outline_result = Runner.run_sync(self.outline_agent, title)
        outline = outline_result.final_output

        _logger.info("Writing content")
        content_result = Runner.run_sync(self.content_agent, outline)
        content = content_result.final_output

        _logger.info("Proofreading content")
        feedback_result = Runner.run_sync(self.proofread_agent, content)
        feedback = feedback_result.final_output

        _logger.info("Applying corrections")
        corrected_result = Runner.run_sync(
            self.content_agent,
            (
                "Please update the blog post with these corrections:\n"
                f"{feedback}\n\nBlog post:\n{content}"
            ),
        )
        return corrected_result.final_output
