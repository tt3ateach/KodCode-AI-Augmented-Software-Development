# Module 1 Cheat Sheet — The AI-Augmented Developer

## Core definition

**AI-augmented software development** is the intentional use of AI systems to assist, accelerate, or partially automate software work across the software development lifecycle, while leaving accountability for correctness, safety, maintainability, and product fit with humans.

The course’s central operating principle:

> AI can accelerate software work, but developers still own the spec, architecture, review, verification, security, and long-term maintainability.

---

## The 2026 shift

| Earlier framing | Current framing |
|---|---|
| “AI helps me write code.” | “AI helps me build a feature.” |
| “Autocomplete in the editor.” | “Agents can inspect, edit, test, and open PRs.” |
| “Prompt quality is enough.” | “Prompting + context + permissions + verification are the work system.” |
| “The main bottleneck is typing.” | “The main bottleneck is review and ownership.” |

Memorable phrase:

> Working code is not yet owned code.

---

## Interaction spectrum

| Mode | What it does | Best for | Review burden |
|---|---|---|---|
| **Coding assistant** | Inline completions, local edits, boilerplate | Short, low-risk tasks | Low |
| **Chat assistant** | Explains, compares, summarizes, suggests | Orientation, questions, design alternatives | Low–Medium |
| **AI pair programmer** | Debugs, refactors, drafts tests/docs, reasons with code context | Daily development work | Medium |
| **IDE agent** | Makes bounded multi-file edits and may run commands | Clear tasks with cheap verification | Medium–High |
| **Coding/cloud agent** | Works asynchronously from issue/task and returns branch/PR | Well-scoped work that can be reviewed as a diff | High |
| **Agentic workflow** | Connects repo, tickets, docs, CI/CD, and tools | Repeated internal workflows | Very High |

Move right only when task clarity and verification improve faster than risk.

---

## Five-question tool-fit heuristic

Before using AI, ask:

1. **How clear is the task?**
2. **How much context is required?**
3. **What is the blast radius if it is wrong?**
4. **Can I verify the result cheaply?**
5. **Do I need a suggestion, or do I need the tool to act?**

### Fast rule of thumb

- Use an **assistant** for local acceleration.
- Use **chat** when explanation or comparison is enough.
- Use a **pair programmer** when reasoning, debugging, or tests matter.
- Use an **IDE agent** when a small multi-file task has clear acceptance criteria.
- Use a **coding/cloud agent** when the task is issue-shaped and reviewable as a PR.
- Use **human-led AI support only** for security, auth, billing, data migrations, production incidents, or hard-to-verify changes.

---

## Tool-fit examples

| Task | Recommended mode | Why |
|---|---|---|
| Rename a misleading local variable | Inline assistant | Local, low risk, easy diff review |
| Explain a legacy parser | Chat / pair programmer | Read-only orientation is valuable |
| Generate tests for a pure utility function | Pair programmer | Useful draft, but assertions need review |
| Add validation to a small isolated function | IDE agent | Bounded change, tests can verify |
| Implement RBAC for production auth | Human-led, AI-assisted | High blast radius and policy/security complexity |
| Modify payment retry logic | Human-led, AI-assisted | High product and financial risk |
| Summarize merged PRs into changelog | Chat / workflow | Low risk if reviewed |
| Create a deployment script | Pair programmer or constrained IDE agent | Useful, but command safety matters |

---

## What current tools usually do well

- Scaffolding and boilerplate
- Explaining unfamiliar code
- Repetitive transformations
- Drafting tests and documentation
- Refactoring familiar patterns
- Repo orientation and search
- Structured work under explicit constraints
- Producing useful first drafts quickly

## What still breaks

- Hidden business rules
- Subtle edge cases
- Security-sensitive defaults
- Authorization and data exposure rules
- Dependency/version assumptions
- External API assumptions
- Generated tests that copy wrong assumptions
- Polished explanations that outrun the code

Important failure mode:

> The answer is often not ridiculous. It is often **plausibly incomplete**.

---

## Human review checklist

Treat AI output like work from a confident, fast, unfamiliar junior contractor.

- [ ] Does it solve the right problem?
- [ ] Did it preserve existing behavior?
- [ ] Are edge cases and failure modes handled?
- [ ] Are validation and error handling explicit?
- [ ] Do tests cover intended behavior, not just implementation details?
- [ ] Did lint, type checks, and tests pass?
- [ ] Did it introduce secrets, insecure defaults, unsafe dependencies, or unsafe logging?
- [ ] Does the code fit team conventions and architecture?
- [ ] Can the change be rolled back?

---

## Privacy / IP / governance

### Usually safe

- Toy code
- Synthetic examples
- Public documentation
- Approved internal summaries
- Redacted stack traces

### Share with caution

- Proprietary code
- Internal architecture details
- Logs and stack traces
- Security-sensitive material
- Non-public product plans

### Never paste

- Secrets, tokens, keys, credentials
- Live customer data
- Regulated personal data
- Production database dumps
- Sensitive customer payloads
- Vulnerability details not approved for the tool/context

---

## MCP preview

MCP lets AI applications connect to external systems: files, databases, tools, prompts, and workflows.

Useful because:

- the assistant can use real context and tools;
- the workflow can move beyond copy/paste;
- teams can standardize tool integrations.

Risky because:

- tool access expands the blast radius;
- permissions and audit logs become critical;
- prompt injection and data-leakage risks become more concrete.

Course phrase:

> The more the assistant can do, the more permissions and review matter.

---

## Do not skip when teaching

- The interaction spectrum
- The five-question decision model
- Plausible incompleteness
- Privacy/IP/security guardrails
- Human ownership of review, verification, and merge

## Safe to skim when short on time

- Vendor-by-vendor ecosystem detail
- MCP mechanics beyond the teaser
- Deep comparisons between similar agent products
