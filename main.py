from __future__ import annotations

import logging
from pathlib import Path

from Agent import Agent


def configure_logging() -> None:
    log_dir = Path("Logs")
    log_dir.mkdir(exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        log_dir / "runtime.log", maxBytes=1_000_000, backupCount=3
    )
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not root_logger.handlers:
        root_logger.addHandler(handler)


def main() -> None:
    configure_logging()
    blog_agent = Agent()
    title = "The Future of AI Collaboration"
    result = blog_agent.run(title)
    print(result)


if __name__ == "__main__":
    main()
