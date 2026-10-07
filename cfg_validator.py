def validate_log_structure(log):
    parts = log.split()

    # CFG structure:
    # LOG → DATE TIME LEVEL MESSAGE

    if len(parts) >= 4:
        date = parts[0]
        time = parts[1]
        level = parts[2]
        message = " ".join(parts[3:])

        if (
            len(date) == 10
            and date[4] == "-"
            and date[7] == "-"
            and len(time) == 8
            and time[2] == ":"
            and time[5] == ":"
            and level in ["INFO", "WARNING", "ERROR"]
            and message
        ):
            return True

    return False