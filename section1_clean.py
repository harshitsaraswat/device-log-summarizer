
import math


def clean_readings(values):
    cleaned = []

    # Handle None as the entire input
    if values is None:
        return []

    for value in values:
        try:
            if value is None:
                continue

            number = float(value)

            # Remove NaN, infinity, and negative values
            if not math.isfinite(number) or number < 0:
                continue

            # Cap values at 500
            if number > 500.0:
                number = 500.0

            cleaned.append(number)

        except (ValueError, TypeError):
            continue

    return cleaned


if __name__ == "__main__":
    print(clean_readings([10, "20.5", None, -3, "abc", 600]))
    print(clean_readings([]))
    print(clean_readings([None, "abc", -5]))
    print(clean_readings(["nan", 5]))
    print(clean_readings(None))
