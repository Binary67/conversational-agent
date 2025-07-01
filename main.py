from __future__ import annotations

import asyncio
import logging
import os
from logging.handlers import RotatingFileHandler

from Agent import run_pipeline


def configure_logging() -> None:
    os.makedirs("Logs", exist_ok=True)
    log_file = "Logs/agents.log"
    if not os.path.exists(log_file):
        open(log_file, "a", encoding="utf-8").close()

    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    logging.basicConfig(level=logging.INFO, handlers=[handler])


def main() -> None:
    configure_logging()
    title = "How to Use OpenAI Agents with Azure"
    result = asyncio.run(run_pipeline(title))
    print(result)


if __name__ == "__main__":
    main()
