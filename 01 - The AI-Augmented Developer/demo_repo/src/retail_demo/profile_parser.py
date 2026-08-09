from dataclasses import dataclass


@dataclass(slots=True)
class UserProfile:
    name: str
    email: str
    age: int | None
    marketing_opt_in: bool


def parse_user_profile(raw: dict) -> UserProfile:
    """
    Parse a user profile submitted by a partner integration.

    This function is intentionally under-defended for Module 1 demos.
    It has enough happy-path behavior to work, but not enough validation
    to be production-ready.
    """
    name = str(raw.get("name", "")).strip().title()
    email = str(raw.get("email", "")).strip().lower()

    age_value = raw.get("age")
    age = int(age_value) if age_value not in (None, "") else None

    marketing_value = str(raw.get("marketing_opt_in", "false")).strip().lower()
    marketing_opt_in = marketing_value in {"true", "1", "yes", "y"}

    return UserProfile(
        name=name,
        email=email,
        age=age,
        marketing_opt_in=marketing_opt_in,
    )
