# Support thread T-219 · short summary (Task E fallback)

The thread's observations in short, without causes.

- 21:18–21:21 UTC: a team lead in Tel Aviv reports that task-42 (to do, due 2026-10-03) became overdue shortly after local midnight, right after she edited a task. The team expected the label to change only when the UTC day changes.
- 21:27: the saved due date is still 2026-10-03.
- 21:28: the server's own clock shows 2026-10-04 00:28.
- 21:30: the API returns `overdue: true` for task-42.
- 21:31: a done task due 2026-10-01 returns `overdue: false`.
- 21:33: a new task created with due date 2026-10-03, with no edit, also returns `overdue: true`.
- Health is green, no extra HTTP 5xx, no disk or database alarms.
- 0.4.1 has been live since 2 October; its only change was PR #31, an AI-assisted tidy-up of date helpers.
- 00:05 UTC on 4 October: task-42 is overdue, which the team expected by then.
- Noise: slow search on the Done tab, a request for recurring reminders, a 404 during a deploy preview, a stale-browser theory.
