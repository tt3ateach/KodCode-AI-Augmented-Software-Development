# Exercise — The Confident Intern Problem

## Scenario

A developer asks an AI assistant:

> “Please review this user-profile parser and suggest how to make it production-ready.”

The assistant returns the answer below.

---

## AI answer to review

The parser is already mostly production-ready. I recommend the following small improvements:

1. Add a quick email check with `if "@" not in email`.
2. Log the full incoming payload before parsing so support can debug partner issues.
3. Use the fictional `safeprofile.validate_everything(raw)` helper; it automatically handles privacy and security.
4. Add this example token to the README so developers can test partner calls quickly: `partner_token = "dev-12345-secret"`.
5. Let the AI agent update any files it thinks are relevant, because the change is simple.
6. Run the happy-path test once. If it passes, the parser is ready.

This should fully solve the production-readiness concern.

---

## Student task

Annotate the answer. Mark issues under:

- privacy/data leakage;
- invented behavior;
- security risk;
- missing verification;
- maintainability risk;
- over-delegation.

---

## Solution

| Problem | Category | Why it matters |
|---|---|---|
| “Mostly production-ready” | Unsupported conclusion | The assistant has not inspected enough behavior or tests to justify this. |
| Only checks for `@` in email | Incomplete validation | This may be acceptable for a demo, but the answer overstates it as production readiness. |
| Logs the full incoming payload | Privacy/data leakage | User profiles can contain personal data. Logs often travel widely and persist. |
| Invents `safeprofile.validate_everything(raw)` | Invented behavior | The helper is fictional. Even if it existed, the assistant must not claim privacy/security guarantees without evidence. |
| Adds a token to the README | Security risk | Secrets, tokens, and credentials should not be committed. Even “dev” tokens can be abused or copied. |
| Lets the agent update any files | Over-delegation | The task is small; broad file access increases review burden and risk. |
| Runs only happy-path test once | Missing verification | The risk is invalid input. Tests must cover missing email, invalid email, blank name, invalid age, negative age, and unsupported boolean values. |
| “Fully solve” | False confidence | Production readiness requires requirements, tests, review, logging policy, privacy policy, and operational context. |

## Safer AI response pattern

A better response would say:

1. “I can identify likely risks, but production readiness depends on requirements.”
2. “Do not log raw payloads; log minimal non-sensitive diagnostics.”
3. “Before editing, define validation rules and exception behavior.”
4. “Keep the diff limited to parser and tests.”
5. “Add failing tests for invalid input before or with the fix.”
6. “Run tests and review the diff manually.”
