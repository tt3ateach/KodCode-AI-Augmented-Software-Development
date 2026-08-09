# Course Tooling Baseline — June 2026

**Course:** AI-Augmented Software Development  
**Prepared for:** Modules 1–7 update/development workflow  
**Access date:** 2026-06-30

This file is the shared reference baseline for current tool/product wording in the course. It is deliberately decision-oriented rather than a product tour. Before teaching or publishing, verify any product-specific UI screenshots and licensing details against the vendor pages, because coding-agent products are changing quickly.

## Teaching stance

- GitHub Copilot is the classroom baseline because students have commercial licenses.
- Vendor names are examples; the durable teaching categories are interaction mode, autonomy level, context surface, permission boundary, and verification burden.
- The course should avoid tool-war debates. Use tools to teach workflows, risk decisions, and review discipline.
- The key judgment question is not “Which tool is best?” but “How much responsibility should I delegate for this task?”

## Interaction modes used throughout the course

| Mode | Typical surface | What the AI can do | Human responsibility |
|---|---|---|---|
| Inline assistant | IDE autocomplete / edits | Suggest code snippets, complete local patterns | Accept/reject local suggestions |
| Chat assistant | IDE/web chat | Explain, compare, draft, reason with context | Provide context, challenge assumptions |
| AI pair programmer | IDE chat + files + tests | Debug, refactor, generate tests/docs, explain diffs | Keep the task bounded and verify output |
| IDE agent | IDE agent mode / terminal-integrated agent | Inspect files, edit multiple files, suggest or run commands | Approve actions, review diff, run checks |
| Coding/cloud agent | Issue/PR/cloud workspace | Work asynchronously from an issue/task and return a branch/PR | Define task, review PR, own merge decision |
| Agentic workflow | Connected tools, CI, tickets, docs | Orchestrate multi-step workflows across systems | Design permissions, approvals, logging, rollback |

## GitHub Copilot — course default

Use Copilot as the common classroom tool. Current Copilot documentation exposes a broad set of concepts and surfaces, including completions, chat, cloud agent, CLI, code review, MCP, repository instructions, prompt files, and enterprise governance. That makes it suitable for teaching the assistant-to-agent progression without requiring students to install many unrelated tools.

Recommended course framing:

- Module 1: Copilot as an example of the interaction spectrum.
- Module 2: Copilot for daily developer workflow: chat, completions, prompt files, repository instructions, code review.
- Module 3: Copilot agent mode as one possible natural-language-led coding surface, with containment.
- Module 5: Copilot review/remediation as helpful but not sufficient.
- Module 6: Copilot/MCP as a tool-connected agent example, not the primary framework.

Official sources:

- GitHub Copilot documentation: https://docs.github.com/en/copilot
- Responsible use of GitHub Copilot features: https://docs.github.com/en/copilot/responsible-use

## Claude Code

Claude Code is a repo-aware coding agent available across terminal, IDE, desktop, and browser surfaces. Official docs describe it as able to read a codebase, edit files, run commands, and integrate with development tools. It also has a permission-based architecture: read-only by default, with explicit approval required for edits and command execution.

Recommended course framing:

- Strong alternative for terminal/IDE-heavy repo work.
- Good example when discussing permissions, `CLAUDE.md`, tool use, and multi-file work.
- Do not make it mandatory for the class unless accounts are available.

Official sources:

- Claude Code overview: https://code.claude.com/docs/en/overview
- Claude Code security: https://code.claude.com/docs/en/security
- Claude Code MCP: https://code.claude.com/docs/en/mcp

## OpenAI Codex

OpenAI’s current Codex documentation presents Codex as a product family across app, IDE extension, CLI, web/cloud, integrations, configuration, permissions, MCP, workflows, and security-oriented features. Treat it as a credible agentic coding alternative, especially for CLI/IDE/cloud-style workflows and parallel/review-oriented coding tasks.

Recommended course framing:

- Mention in Module 1 as part of the agentic coding landscape.
- Use in Module 3 or 6 only as optional comparison, not as a required setup.
- Emphasize review, sandboxing, and permissions rather than “autonomous engineer” claims.

Official sources:

- Codex docs: https://developers.openai.com/codex
- Codex CLI docs: https://developers.openai.com/codex/cli
- Codex in ChatGPT help: https://help.openai.com/en/articles/11369540-codex-in-chatgpt

## Google ecosystem: Gemini Code Assist and Antigravity

As of the latest Google Cloud docs checked for this course, Gemini Code Assist Standard and Enterprise continue to exist for organization-oriented development workflows, while Google states that tools for individuals / Google AI Pro / Google AI Ultra tiers have moved toward a unified multi-agent platform called Antigravity. Google’s docs also note that Gemini CLI and Gemini Code Assist IDE Extensions stopped serving requests for those affected individual tiers starting June 18, 2026.

Recommended course framing:

- Say “Google’s coding ecosystem has shifted toward Antigravity for individual/pro agentic workflows; Gemini Code Assist remains relevant in Standard/Enterprise contexts.”
- Avoid outdated wording that presents Gemini CLI as the stable default individual workflow without qualification.
- Do not build course setup around Google tooling unless the instructor explicitly chooses it.

Official sources:

- Google Antigravity: https://antigravity.google/
- Gemini Code Assist overview: https://docs.cloud.google.com/gemini/docs/codeassist/overview
- Gemini CLI docs: https://docs.cloud.google.com/gemini/docs/codeassist/gemini-cli

## Continue

Continue remains relevant as an open-source/customizable coding-assistant ecosystem and is useful for discussing local/self-hosted or model-flexible workflows. It should be mentioned as an example, not used as a mandatory setup in this course.

Official sources:

- Continue docs: https://docs.continue.dev/
- Continue homepage: https://continue.dev/

## OpenHands

OpenHands is relevant as an open/self-hosted developer control center for coding agents and automations. Its GitHub README describes the project as able to run OpenHands, Claude Code, Codex, Gemini, or ACP-compatible agents across local, remote, and cloud backends.

Recommended course framing:

- Mention as an open/self-hosted option.
- Useful in Module 3/6 for discussing local control, sandboxing, and operational overhead.
- Avoid turning this course into an OpenHands setup workshop.

Official sources:

- OpenHands GitHub: https://github.com/OpenHands/OpenHands
- OpenHands docs: https://docs.openhands.dev/overview/introduction

## Model Context Protocol (MCP)

MCP is an open standard for connecting AI applications to external systems such as files, databases, tools, prompts, and workflows. The course should introduce MCP gradually: a short preview in Module 1, practical risk framing in Modules 3 and 5, and fuller workflow design in Module 6.

Recommended teaching line:

> The more the assistant can do, the more permissions and review matter.

Official source:

- MCP introduction: https://modelcontextprotocol.io/docs/getting-started/intro

## Course-wide cautions

- Do not promise deterministic AI output in live demos.
- Do not let demo agents touch real production systems.
- Prefer prepared fallback artifacts for every live AI demo.
- Avoid using “AI wrote it” as evidence of correctness.
- Treat vendor claims as capabilities to evaluate, not guarantees to rely on.
