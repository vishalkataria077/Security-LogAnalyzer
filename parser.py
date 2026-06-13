import re

def parse_log(file_path):

    events = []

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:

        failed = re.search(
            r"Failed password for (\w+) from ([\d\.]+)",
            line
        )

        accepted = re.search(
            r"Accepted password for (\w+) from ([\d\.]+)",
            line
        )

        if failed:

            events.append({
                "event": "failed_login",
                "user": failed.group(1),
                "ip": failed.group(2)
            })

        elif accepted:

            events.append({
                "event": "successful_login",
                "user": accepted.group(1),
                "ip": accepted.group(2)
            })

    return events