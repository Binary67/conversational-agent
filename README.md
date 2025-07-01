# 📝 Multi-Agent Blog Generator

Harness the power of the **OpenAI Agents SDK** to automate every step of writing a polished blog post. Three specialised agents—an **Outline Writer**, **Content Writer**, and **Proof-reader**—collaborate in a single workflow to deliver ready-to-publish Markdown.

---

## ✨ Key Features

| Agent          | Role                                                       | Highlights                                                          |
| -------------- | ---------------------------------------------------------- | ------------------------------------------------------------------- |
| Outline Writer | Drafts a logical heading structure based on a topic prompt | Ensures SEO-friendly hierarchy, suggested word counts               |
| Content Writer | Expands each heading into engaging paragraphs              | Pulls factual data via retrieval tools and injects examples & CTA’s |
| Proof-reader   | Polishes grammar, tone, and consistency                    | Enforces style guide, fixes links & code blocks                     |

Together they form a **pipeline** orchestrated by a Coordinator class that streams intermediate results between agents until the blog is complete.
