def correlate(alerts):

    incidents = []

    brute_ips = set()
    success_ips = set()
    privileged_ips = set()

    for alert in alerts:

        if "Brute Force Attack" in alert:
            ip = alert.split("from ")[-1]
            brute_ips.add(ip)

        elif "Successful Login After Brute Force" in alert:
            ip = alert.split("from ")[-1]
            success_ips.add(ip)

        elif "Privileged Account Login" in alert:
            ip = alert.split("from ")[-1]
            privileged_ips.add(ip)

    for ip in brute_ips:

        if ip in success_ips and ip in privileged_ips:

            incidents.append({
                "severity": "CRITICAL",
                "ip": ip,
                "description": "Full Attack Chain Detected"
            })

        elif ip in success_ips:

            incidents.append({
                "severity": "CRITICAL",
                "ip": ip,
                "description": "Possible Account Compromise"
            })

    return incidents