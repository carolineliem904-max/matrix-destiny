from datetime import date


def validate_birth_date(birth_date: date) -> None:
    today = date.today()
    if birth_date > today:
        raise ValueError("Birth date cannot be in the future.")
    if birth_date.year < 1900:
        raise ValueError("Birth date must be 1900 or later for this MVP.")
