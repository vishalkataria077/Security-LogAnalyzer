# AI Security Log Analyzer

A Python-based cybersecurity project that analyzes authentication logs, detects suspicious activity, extracts indicators of compromise (IOCs), and generates incident reports.

## Features

* Log Parsing
* Brute Force Detection
* Successful Login After Brute Force Detection
* MITRE ATT&CK Mapping (T1110)
* IOC Extraction
* Risk Scoring
* Incident Report Generation

## Example Detection

Input Log:

Failed password for admin from 192.168.1.50
Failed password for admin from 192.168.1.50
Failed password for admin from 192.168.1.50
Accepted password for admin from 192.168.1.50

Output:

[HIGH] T1110 Brute Force Attack from 192.168.1.50

[CRITICAL] T1110 Successful Login After Brute Force from 192.168.1.50

Risk Score: 10/10

## Project Structure

ai-log-analyzer/

├── parser.py

├── detector.py

├── ioc.py

├── report.py

├── main.py

├── sample.log

└── incident_report.txt

## Roadmap

* Web Dashboard (Flask)
* AI Alert Explanations
* Additional Detection Rules
* PDF Reporting
* Threat Intelligence Integration
