from datetime import datetime

def generate_report(alerts, risk_score):

    with open("incident_report.txt", "w") as report:

        report.write("SECURITY INCIDENT REPORT\n")
        report.write("=" * 30 + "\n\n")

        report.write(
            f"Generated: {datetime.now()}\n\n"
        )

        report.write(
            f"Risk Score: {risk_score}/10\n\n"
        )

        report.write("Alerts:\n\n")

        for alert in alerts:
            report.write(f"- {alert}\n")