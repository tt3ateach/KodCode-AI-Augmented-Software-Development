# Support thread · simulated

Opened on 3 October at 21:30 UTC, which is 00:30 on 4 October in Tel Aviv.

**Team lead:** Just after midnight our time, task-42 (due 2026-10-03, not done) started showing "Overdue". Our planning doc says that should only happen when the UTC day changes, at 03:00 our time. I had just edited the task.

**Support:** Refreshing doesn't help, and a colleague sees the same on another laptop.

**Support:** Separate ticket: search on the Done tab feels slow.

**QA:** The saved due date is still 2026-10-03. A new task due 2026-10-03, never edited, shows "Overdue" too.

**QA:** The API itself returns `"overdue": true` for both tasks.

**Support:** Could it be a stale value cached in the browser?

**Operations:** Health is green. This instance runs on the Tel Aviv office's own server, which is set to local time. The server and the team's laptops all show 00:30 on 4 October.

**Operations:** The only change this week was release 0.4.1, an AI-assisted tidy-up of date helpers: "no behavior change intended".

**Support:** Another user asks for email reminders. Logged as a separate request.

**Team lead, three hours later:** Since 03:00 our time, everything looks as expected.
