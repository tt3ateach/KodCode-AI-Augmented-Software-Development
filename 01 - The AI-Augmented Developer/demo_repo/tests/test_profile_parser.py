from retail_demo.profile_parser import UserProfile, parse_user_profile


def test_parse_user_profile_happy_path():
    raw = {
        "name": "  ada lovelace ",
        "email": " ADA@example.COM ",
        "age": "36",
        "marketing_opt_in": "yes",
    }

    assert parse_user_profile(raw) == UserProfile(
        name="Ada Lovelace",
        email="ada@example.com",
        age=36,
        marketing_opt_in=True,
    )


def test_parse_user_profile_without_optional_age():
    raw = {
        "name": "grace hopper",
        "email": "grace@example.com",
        "marketing_opt_in": "false",
    }

    profile = parse_user_profile(raw)

    assert profile.age is None
    assert profile.marketing_opt_in is False
