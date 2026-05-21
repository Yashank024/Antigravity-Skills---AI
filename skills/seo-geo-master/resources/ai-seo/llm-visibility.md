# AI SEO: LLM Visibility

If an AI crawler cannot access or understand a website, that brand ceases to exist in modern generative search.

## 1. Validating Crawler Access
- The agent must always check `robots.txt` for AI crawler blocks.
- **Vital Bots to Allow**: 
  - `GPTBot` (OpenAI training)
  - `ChatGPT-User` (ChatGPT web browsing)
  - `Google-Extended` (Google AI Overviews)
  - `PerplexityBot` (Perplexity AI)
  - `ClaudeBot` (Anthropic)
- If a client has arbitrarily blocked all bots, the agent must warn them of the catastrophic loss of LLM visibility.

## 2. Implementing `llms.txt`
- AI systems now actively look for an `/llms.txt` and `/llms-full.txt` file at the root of a domain.
- This file acts as a curated reading list specifically formatted for RAG ingestion.
- **Agent Action**: The agent must generate or verify the presence of this file, ensuring it contains absolute URLs to the brand's most critical "Hub" content.

## 3. Brand Entity Extraction
- Test the brand's AI visibility by executing 0-shot prompts against the major LLMs.
- Example prompt: "Summarize the core features of [Brand Name] software."
- If the AI hallucinates, it means the brand's entity graph is weak. The solution is massive PR distribution and strict `Organization` Schema deployment.
