import sqlite3


def init_db():

    conn = sqlite3.connect("alerts.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            severity TEXT,
            ip TEXT,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_alert(severity, ip, description):

    conn = sqlite3.connect("alerts.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO alerts
        (
            severity,
            ip,
            description
        )
        VALUES (?, ?, ?)
        """,
        (
            severity,
            ip,
            description
        )
    )

    conn.commit()
    conn.close()


def get_alerts():

    conn = sqlite3.connect("alerts.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            timestamp,
            severity,
            ip,
            description
        FROM alerts
        ORDER BY id DESC
        """
    )

    alerts = cursor.fetchall()

    conn.close()

    return alerts