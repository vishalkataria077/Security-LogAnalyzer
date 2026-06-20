from flask import (
    Flask,
    render_template,
    request,
    Response
)

from parser import parse_log
from detector import analyze_events
from ioc import extract_iocs
from correlation import correlate

from database import (
    init_db,
    save_alert,
    save_incident,
    get_alerts,
    get_incidents
)

app = Flask(__name__)

init_db()


@app.route("/", methods=["GET", "POST"])
def dashboard():

    alerts = []
    incidents = []
    iocs = []
    techniques = []

    risk_score = 0

    total_events = 0
    failed_logins = 0
    successful_logins = 0

    high_alerts = 0
    medium_alerts = 0
    critical_alerts = 0

    if request.method == "POST":

        file = request.files["logfile"]

        if file:

            file.save("uploaded.log")

            events = parse_log("uploaded.log")

            alerts = analyze_events(events)

            incidents = correlate(alerts)

            if any("T1110" in alert for alert in alerts):

                techniques.append(
                    ("T1110", "Brute Force")
                )

            if any("T1078" in alert for alert in alerts):

                techniques.append(
                    ("T1078", "Valid Accounts")
                )

            iocs = extract_iocs(events)

            high_alerts = len(
                [a for a in alerts if "[HIGH]" in a]
            )

            medium_alerts = len(
                [a for a in alerts if "[MEDIUM]" in a]
            )

            critical_alerts = len(
                [a for a in alerts if "[CRITICAL]" in a]
            )

            for alert in alerts:

                severity = "HIGH"

                if "[CRITICAL]" in alert:
                    severity = "CRITICAL"

                elif "[MEDIUM]" in alert:
                    severity = "MEDIUM"

                ip = "Unknown"

                if "from " in alert:
                    ip = alert.split("from ")[-1]

                save_alert(
                    severity,
                    ip,
                    alert
                )

            for incident in incidents:

                save_incident(
                    incident["severity"],
                    incident["ip"],
                    incident["description"]
                )

            risk_score = min(
                len(alerts) * 5,
                10
            )

            total_events = len(events)

            failed_logins = len(
                [
                    e for e in events
                    if e["event"] == "failed_login"
                ]
            )

            successful_logins = len(
                [
                    e for e in events
                    if e["event"] == "successful_login"
                ]
            )

    return render_template(
        "index.html",
        alerts=alerts,
        incidents=incidents,
        iocs=iocs,
        techniques=techniques,
        risk_score=risk_score,
        total_events=total_events,
        failed_logins=failed_logins,
        successful_logins=successful_logins,
        high_alerts=high_alerts,
        medium_alerts=medium_alerts,
        critical_alerts=critical_alerts
    )


@app.route("/history")
def history():

    severity = request.args.get(
        "severity",
        "ALL"
    )

    ip = request.args.get(
        "ip",
        ""
    )

    alerts = get_alerts(
        severity,
        ip
    )

    return render_template(
        "history.html",
        alerts=alerts,
        severity=severity,
        ip=ip
    )


@app.route("/export")
def export_csv():

    alerts = get_alerts()

    def generate():

        yield "Timestamp,Severity,IP,Description\n"

        for alert in alerts:

            yield (
                f"{alert[0]},"
                f"{alert[1]},"
                f"{alert[2]},"
                f"\"{alert[3]}\"\n"
            )

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=alerts.csv"
        }
    )


if __name__ == "__main__":
    app.run(debug=True)