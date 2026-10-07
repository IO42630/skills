def milliseconds_to_seconds(milliseconds):
    if milliseconds < 0:
        raise ValueError("timeout must be non-negative")
    return milliseconds / 1000


def request_options(milliseconds):
    return {
        "timeout": milliseconds_to_seconds(milliseconds),
        "retries": 2,
    }