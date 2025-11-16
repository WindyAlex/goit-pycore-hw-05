import sys
import re


def parse_log_line(line: str) -> dict:
    line = line.strip()
    if not line:
        print("Empty log line")
        return

    matched_line = re.match(
            r"^\s*(\d{4}-\d{2}-\d{2})\s+"
            r"(\d{2}:\d{2}:\d{2})\s+"
            r"([A-Za-z]+)\s*"
            r"(.*)\s*$",
            line,
    )

    if not matched_line:
        print("Log line has wrong format")
        return None

    date, time, level, message = matched_line.groups()
    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message,
    }


def load_logs(file_path: str) -> list[dict]:
    logs: list[dict] = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            logs = [
                parsed
                for line in f
                if (parsed := parse_log_line(line)) is not None
            ]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' was not found")
        sys.exit(1)
    except OSError as e:
        print(f"Can not read file '{file_path}': {e}")
        sys.exit(1)

    return logs


def filter_logs_by_level(logs: list[dict], level: str) -> list[dict]:

    level_upper = level.upper()
    return [log for log in logs if log["level"].upper() == level_upper]


def count_logs_by_level(logs: list[dict]) -> dict:
    counts: dict[str, int] = {}
    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts


def display_log_counts(counts: dict) -> None:
    levels_order = ["INFO", "DEBUG", "ERROR", "WARNING"]

    print("Рівень логування | Кількість")
    print("-----------------|----------")

    for level in levels_order:
        count = counts.get(level, 0)
        print(f"{level:<16} | {count}")


def display_logs_for_level(logs: list[dict], level: str) -> None:
    print(f"\nLogs for Level: [{level.upper()}]:")
    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py path/to/logfile.log [level]")
        sys.exit(1)

    file_path = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) >= 3 else None

    logs = load_logs(file_path)
    if not logs:
        print("File is empty or data is invalid")
        sys.exit(0)

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level:
        filtered_logs = filter_logs_by_level(logs, level)
        if not filtered_logs:
            print(f"\nNo logs for level '{level.upper()}'.")
        else:
            display_logs_for_level(filtered_logs, level)


main()
