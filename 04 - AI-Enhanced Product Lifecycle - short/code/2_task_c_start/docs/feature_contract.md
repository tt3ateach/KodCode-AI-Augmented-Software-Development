# Classroom feature contract
These are the decisions the class agreed after Task A. They are product decisions, not facts an assistant could have inferred from the original request.

| ID | Agreed behavior | Example |
|---|---|---|
| REQ-01 | A due date is optional. | Old create requests still work and return a null date. |
| REQ-02 | Accept `YYYY-MM-DD` or null. Reject invalid dates/timestamps with 422. | `2026-02-30` is invalid. |
| REQ-03 | A PATCH omission retains the date. Explicit null clears it. | Changing the title keeps the date. Clearing survives a later GET. |
| REQ-04 | Overdue means strictly before the server's UTC calendar day. Calculate it on reads. | On 2026-10-04, Oct 3 is overdue and Oct 4 is not. |
| REQ-05 | Completed tasks are never overdue. | Reopening a completed past-due task makes it overdue again. |
| REQ-06 | Overdue only returns exactly the unfinished past-due tasks and respects other filters. | Check task IDs, not only a count. |
| REQ-07 | Persist dates and preserve old rows through an additive migration. | Old tasks acquire a null date. No stored overdue flag. |
| REQ-08 | Enter/clear dates and show overdue in text. | A date control, Overdue only control, readable labels and keyboard checks. |

**Given/When/Then:** Given an unfinished task due Oct 4 and a UTC reference day of Oct 4, when I read it, then overdue is false.

**Given/When/Then:** Given a task with a saved date, when I PATCH `due_date: null` and read it again, then its date is null and its title remains unchanged.

Reminders, recurrence, accounts and cloud rollout stay outside the first release. Reminder delivery needs its own discovery item. Existing `/work-items` endpoints, status values and old clients remain compatible.
