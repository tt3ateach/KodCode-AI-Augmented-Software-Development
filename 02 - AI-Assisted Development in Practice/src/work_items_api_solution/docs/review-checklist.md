# AI-Assisted Diff Review Checklist

- [ ] Does the diff implement only the requested scope?
- [ ] Are endpoint paths and response shapes unchanged unless approved?
- [ ] Are user-controlled values handled safely?
- [ ] Do tests assert payload behavior, not only status codes?
- [ ] Are negative cases covered?
- [ ] Did AI introduce unrelated dependencies or refactors?
- [ ] Are errors and edge cases understandable?
- [ ] Did the author run `pytest -q`?
- [ ] Is there a rollback or revert path if needed?
