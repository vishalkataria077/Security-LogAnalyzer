def extract_iocs(events):

    ips = set()

    for event in events:

        ips.add(event["ip"])

    return list(ips)