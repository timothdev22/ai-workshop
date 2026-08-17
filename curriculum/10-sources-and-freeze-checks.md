# Sources and update notes

These sources support current tooling choices and the workshop's evidence-first approach. Recheck time-sensitive technical pages during the one-week freeze:

- [Official OpenAI documentation for `gpt-oss-120b`](https://developers.openai.com/api/docs/models/gpt-oss-120b)
- [Nscale chat integration guide](https://docs.nscale.com/docs/use-cases/chat)
- [Nscale model discovery documentation](https://docs.nscale.com/docs/ai-services/models)
- [Nscale Chat Completions API reference](https://docs.nscale.com/api-reference/inference/create-chat-completion)
- [Nscale service-token deprecation note](https://docs.nscale.com/docs/faqs/deprecations)
- [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP transports specification](https://modelcontextprotocol.io/specification/draft/basic/transports)
- [MCP security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [Cline MCP documentation](https://docs.cline.bot/mcp/mcp-overview)
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [OpenAI agent evaluation guidance](https://developers.openai.com/api/docs/guides/agent-evals)
- [Hugging Face PEFT quick tour](https://huggingface.co/docs/peft/quicktour)
- [NIST AI Risk Management Framework](https://airc.nist.gov/airmf-resources/airmf/)
- [OWASP GenAI Security Project](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- [World Economic Forum Future of Jobs skills outlook](https://www.weforum.org/publications/the-future-of-jobs-report-2025/in-full/3-skills-outlook/)
- [Stack Overflow 2025 AI developer survey](https://survey.stackoverflow.co/2025/ai)

## Items to verify during the freeze

- exact Nscale model ID and service-token distribution method
- Nscale tool-calling response shape for the selected model
- available embedding model and fallback index
- current stable MCP Python SDK and compatible Cline configuration
- current Cline settings path and transport field names
- fine-tuning model license, Colab compatibility, and pinned package versions
- Coolify deployment route, domain, TLS, resource limits, and rollback steps
- whether any institutional privacy or data-retention rule changes the labs
