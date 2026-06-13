def analyze_events(events):

    failed_count = {}

    failed_users = {}

    successful_ips = set()

    alerts = []

    for event in events:

        ip = event["ip"]

        user = event["user"]

        if event["event"] == "failed_login":

            failed_count[ip] = (
                failed_count.get(ip, 0) + 1
            )

            if ip not in failed_users:
                failed_users[ip] = set()

            failed_users[ip].add(user)

        elif event["event"] == "successful_login":

            successful_ips.add(ip)

            # MITRE ATT&CK T1078 - Valid Accounts
            if user.lower() in [
                "admin",
                "root",
                "administrator"
            ]:

                alerts.append(
                    f"[MEDIUM] T1078 Privileged Account Login ({user}) from {ip}"
                )

    # Password Spray Detection

    for ip, users in failed_users.items():

        if len(users) >= 3:

            alerts.append(
                f"[HIGH] Password Spraying Attack from {ip}"
            )

    # Brute Force Detection

    for ip, count in failed_count.items():

        user_count = len(
            failed_users.get(ip, set())
        )

        if count >= 3 and user_count < 3:

            alerts.append(
                f"[HIGH] T1110 Brute Force Attack from {ip}"
            )

            if ip in successful_ips:

                alerts.append(
                    f"[CRITICAL] T1110 Successful Login After Brute Force from {ip}"
                )

    return alerts