"""Main module for the third task."""

from typing import Callable, Tuple
from collections import Counter
from datetime import datetime
from enum import Enum, auto
from dataclasses import dataclass
import sys

class LogLevel(Enum):
    """Enum for log levels."""
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()

@dataclass
class LogMessage():
    """Dataclass for a log message."""
    datetime: datetime
    level: LogLevel
    message: str

    def __str__(self):
        return f"{self.datetime} - {self.message}"

Parser = Callable[[str], LogMessage]

def parse_log_line(line: str) -> Tuple[LogMessage, str]:
    """Parse a log line into a LogMessage object."""
    parts = line.split(' ')
    return LogMessage(
        datetime=datetime.fromisoformat(" ".join(parts[:2])),
        level=LogLevel[parts[2]],
        message=" ".join(parts[3:]).rstrip()
    )

def load_logs(logs_path: str, parser: Parser) -> Tuple[list[LogMessage], str]:
    """Load logs from a file and parse them using the provided parser."""

    try:
        with open(logs_path, 'r', encoding='utf-8') as file:
            return list(map(parser, file.readlines())), None
    except FileNotFoundError:
        return [], f'File not found: {logs_path}'
    except PermissionError:
        return [], f'Permission denied for file: {logs_path}'
    except IsADirectoryError:
        return [], f'File is a directory: {logs_path}'
    except KeyError as e:
        return [], f'Invalid log level in log file: {e}'
    except Exception as e:
        return [], str(e)

def count_logs_by_level(logs: list[LogMessage]) -> dict[LogLevel, int]:
    """Count the number of logs for each log level."""
    return Counter(map(lambda log: log.level, logs))

def display_log_counts(logs_by_level: dict[LogLevel, int]):
    """Display the number of logs for each log level."""
    table = []
    table.append("Log levels │ Count")
    table.append("───────────┼──────")
    for log_level, count in logs_by_level.items():
        table.append(f"{log_level.name:<10} │ {count}")

    return "\n".join(table)

def display_logs_of_level(logs: list[LogMessage], level: LogLevel):
    """Display logs of a specific level."""
    return f"Logs of level {level.name}:\n" \
          + "\n".join(map(str, filter(lambda log: log.level == level, logs)))

def main(logs_path: str, level: LogLevel = None):
    """Main function for the third task."""

    logs, err = load_logs(logs_path, parse_log_line)
    if err:
        print(f"Error loading logs: {err}")
        return

    logs_by_level = count_logs_by_level(logs)

    table = display_log_counts(logs_by_level)

    print(table)

    if level:
        print()
        print(display_logs_of_level(logs, level))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py <path> [log_level]')
        sys.exit(1)
    path = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            main(path, LogLevel[sys.argv[2]])
        except KeyError:
            print('Invalid log level. Available levels: DEBUG, INFO, WARNING, ERROR')
            sys.exit(1)
    else:
        main(path)
