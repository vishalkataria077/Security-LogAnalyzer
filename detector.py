def analyze_events(events):

    failed_count = {}

    successful_ips = set()

    alerts = []

    for event in events:

        ip = event["ip"]

        if event["event"] == "failed_login":

            failed_count[ip] = (
                failed_count.get(ip, 0) + 1
            )

        elif event["event"] == "successful_login":

            successful_ips.add(ip)

    for ip, count in failed_count.items():

        if count >= 3:

            alerts.append(
                f"[HIGH] T1110 Brute Force Attack from {ip}"
            )

            if ip in successful_ips:

                alerts.append(
                    f"[CRITICAL] T1110 Successful Login After Brute Force from {ip}"
                )

    return alerts