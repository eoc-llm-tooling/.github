# eoc-llm-tooling

Single-purpose tools for running local LLMs and serving MCP servers to agents. Each repository
does one job and can be used on its own.

| Repository | What it does |
|---|---|
| [local-llm-serve](https://github.com/eoc-llm-tooling/local-llm-serve) | starts OVMS, Ollama and llama.cpp on the local machine, and prepares the models they load |
| [mcp-call-orchestrator-proxy](https://github.com/eoc-llm-tooling/mcp-call-orchestrator-proxy) | makes one MCP server safe for many concurrent clients: serialized calls, self-healing connection, exact parity with the backend |

Contributions follow [CONTRIBUTING.md](https://github.com/eoc-llm-tooling/.github/blob/main/CONTRIBUTING.md).
All repositories are MIT-licensed.
