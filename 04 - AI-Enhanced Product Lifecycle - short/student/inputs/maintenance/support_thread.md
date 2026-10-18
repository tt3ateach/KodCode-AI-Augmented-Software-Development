# Support thread T-219 · simulated

Line times are UTC, as recorded by the support tool. Clock readings quoted inside a message are as reported.

2026-10-03 21:18 · Support: New report from the Tel Aviv team. Overdue labels changed shortly after midnight their time.


21:19 · Team lead: It happened right after I edited a task. I may have changed the date and the title.


21:20 · Support: Which task, and which date?


21:21 · Team lead: task-42, due 2026-10-03, not finished. Our planning doc says a task only becomes overdue when the UTC day changes. We schedule late reviews around that. It is now overdue already.


21:22 · Support: Does refreshing change it?


21:23 · Team lead: No. A colleague sees the same thing on another laptop.


21:24 · Support: A separate ticket mentions slow search on the Done tab. Different view, probably unrelated.


21:25 · Operations: Health is green. No increase in HTTP 5xx.


21:26 · QA: Could the title edit have changed the date field? Compare the API response with the saved row.


21:27 · QA: The saved row for task-42 still has due_date 2026-10-03.


21:28 · Operations: The server's own clock currently shows 2026-10-04 00:28.


21:29 · Support: Browser locale is Hebrew; the laptop clock reads the same as the server's.


21:30 · API sample: task-42 is todo, due_date 2026-10-03, overdue true.


21:31 · QA: A done task due 2026-10-01 returns overdue false.


21:32 · Support: Can anyone reproduce it without editing anything?


21:33 · QA: A brand-new task created with due_date 2026-10-03 also returns overdue true. No PATCH involved.


21:34 · Operations: 0.4.1 has been live since 2 October. Its release record is attached.


21:35 · Support: Another user asks for recurring reminders. Logged as a separate request.


21:36 · Operations: One static asset returned 404 during an unrelated deploy preview; live pages return 200.


21:37 · Support: Could it be a stale flag cached in the browser?


21:38 · Operations: Disk, memory and database connections look normal.


21:39 · Support: Please keep the exact task, date and times in the ticket summary.
2026-10-04 00:05 · Team lead: It is 03:05 here. task-42 is overdue now, which is what we expected today.
00:06 · Support: The team says the odd behavior lasted "a few hours". We only have samples from the start and the end of that period.
