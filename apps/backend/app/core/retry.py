from datetime import UTC, datetime, timedelta

MAX_RETRIES = 5


def calculate_next_retry(attempt: int) -> datetime:
    delay = min(2**attempt, 300)

    return datetime.now(UTC) + timedelta(seconds=delay)
