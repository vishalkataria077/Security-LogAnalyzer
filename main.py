from parser import parse_log
from detector import analyze_events
from report import generate_report
from ioc import extract_iocs

events = parse_log("sample.log")

alerts = analyze_events(events)

iocs = extract_iocs(events)

risk_score = min(len(alerts) * 5, 10)

print(f"\nRisk Score: {risk_score}/10\n")

print("SECURITY ALERTS\n")

for alert in alerts:
    print(alert)

print("\nIndicators of Compromise:")

for ip in iocs:
    print("-", ip)

generate_report(alerts, risk_score)

print("\nIncident report generated.")