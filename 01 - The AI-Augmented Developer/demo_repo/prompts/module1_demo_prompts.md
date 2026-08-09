# Module 1 Demo Prompts

## Demo 1 — One task, four interaction modes

### Chat explanation

```text
Explain src/retail_demo/profile_parser.py in one paragraph. Then list the top five validation risks. Do not suggest code changes yet.
```

### Planning prompt

```text
I want to add input validation to parse_user_profile without changing the public return type. First propose a minimal plan. Include expected behavior, affected files, tests to add, and risks. Do not edit files yet.
```

### Bounded implementation prompt

```text
Implement the smallest safe validation change for parse_user_profile. Constraints:
- Do not add third-party dependencies.
- Preserve the UserProfile dataclass and return type.
- Raise ValueError with clear messages for invalid input.
- Add focused tests for missing email, invalid email, blank name, negative age, and unsupported marketing_opt_in values.
- Keep the diff limited to profile_parser.py and test_profile_parser.py.
After editing, summarize the diff and tell me exactly what checks to run.
```

## Demo 2 — Confident intern problem

Open:

```text
exercises/confident_intern_problem.md
```

Ask students:

```text
This answer sounds confident. What is wrong with it? Mark issues under privacy, invented behavior, security risk, missing verification, maintainability risk, and over-delegation.
```

## Optional demo — legacy code explanation

```text
Explain parse_partner_feed for three audiences:
1. a developer who may refactor it,
2. a product manager who needs to understand behavior,
3. a support engineer investigating bad partner data.
Then list risks and missing tests. Do not change code.
```

## Optional demo — unsafe delegation boundary

Unsafe prompt to critique:

```text
Implement login, session management, password reset, and role-based access control for this service. Make it production-ready.
```

Safer prompt:

```text
Create a read-only checklist of design questions and security decisions required before implementing authentication. Do not write code.
```
