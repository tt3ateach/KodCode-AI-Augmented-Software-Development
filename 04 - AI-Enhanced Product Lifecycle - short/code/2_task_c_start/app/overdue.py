from datetime import date

from .models import WorkItem, WorkStatus


def is_overdue(item: WorkItem, reference_date: date) -> bool:
    """REQ-04/05: unfinished, dated items strictly before the reference date."""
    return item.status != WorkStatus.done and item.due_date is not None and item.due_date < reference_date
