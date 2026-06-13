from flask import Flask, render_template, request
from parser import parse_log
from detector import analyze_events
from ioc import extract_iocs

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def dashboard():

    alerts = []
    iocs = []
    risk_score = 0

    total_events = 0
    failed_logins = 0
    successful_logins = 0

    if request.method == "POST":

        file = request.files["logfile"]

        if file:

            file.save("uploaded.log")

            events = parse_log("uploaded.log")

            alerts = analyze_events(events)

            iocs = extract_iocs(events)

            risk_score = min(len(alerts) * 5, 10)

            total_events = len(events)

            failed_logins = len(
                [e for e in events if e["event"] == "failed_login"]
            )

            successful_logins = len(
                [e for e in events if e["event"] == "successful_login"]
            )

    return render_template(
        "index.html",
        alerts=alerts,
        iocs=iocs,
        risk_score=risk_score,
        total_events=total_events,
        failed_logins=failed_logins,
        successful_logins=successful_logins
    )

if __name__ == "__main__":
    app.run(debug=True)