from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass

from agents import Agent, Runner, RunConfig
from agents.models.openai_provider import OpenAIProvider
from openai import AsyncAzureOpenAI

logger = logging.getLogger(__name__)


@dataclass
class BlogContext:
    title: str
    outline: str | None = None
    draft: str | None = None
    proofread_notes: str | None = None


class AgentCoordinator:
    def __init__(self) -> None:
        client = AsyncAzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        )
        self.provider = OpenAIProvider(openai_client=client)
        self.OutputFile = "Logs/agents_output.txt"
        os.makedirs("Logs", exist_ok=True)
        if not os.path.exists(self.OutputFile):
            open(self.OutputFile, "a", encoding="utf-8").close()
        self.outline_agent = Agent(
            name="Outline Writer",
            instructions=(
                "You create concise blog outlines. Provide a numbered list of sections "
                "for the given title."
            ),
        )
        self.content_agent = Agent(
            name="Content Writer",
            instructions=(
                "Write the blog post in markdown based on the provided outline."
                " When given proofreading feedback, apply the corrections and return the updated blog."
            ),
        )
        self.proofread_agent = Agent(
            name="Proofread Writer",
            instructions=(
                "Review the blog post and list grammar or spelling mistakes that should be fixed."
            ),
        )

    def SaveOutput(self, agent_name: str, content: str) -> None:
        with open(self.OutputFile, "a", encoding="utf-8") as file:
            file.write(f"### Output from {agent_name}\n{content}\n\n")

    async def generate_blog(self, title: str) -> str:
        context = BlogContext(title=title)
        run_config = RunConfig(model_provider=self.provider)

        logger.info("Running Outline Writer")
        outline_result = await Runner.run(self.outline_agent, title, run_config=run_config)
        context.outline = outline_result.final_output
        self.SaveOutput("Outline Writer", context.outline)

        logger.info("Running Content Writer for first draft")
        draft_input = f"Title: {title}\nOutline:\n{context.outline}"
        draft_result = await Runner.run(self.content_agent, draft_input, run_config=run_config)
        context.draft = draft_result.final_output
        self.SaveOutput("Content Writer Draft", context.draft)

        logger.info("Running Proofread Writer")
        proofread_result = await Runner.run(self.proofread_agent, context.draft, run_config=run_config)
        context.proofread_notes = proofread_result.final_output
        self.SaveOutput("Proofread Writer", context.proofread_notes)

        logger.info("Applying proofreading corrections")
        correction_input = (
            f"Original Content:\n{context.draft}\n\nCorrections:\n{context.proofread_notes}\n"
            "Return the corrected blog post in markdown."
        )
        final_result = await Runner.run(self.content_agent, correction_input, run_config=run_config)
        self.SaveOutput("Content Writer Final", final_result.final_output)
        return final_result.final_output


async def run_pipeline(title: str) -> str:
    coordinator = AgentCoordinator()
    return await coordinator.generate_blog(title)


if __name__ == "__main__":
    result = asyncio.run(run_pipeline("Sample Blog Title"))
    print(result)
