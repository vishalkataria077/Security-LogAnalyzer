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


def alert_exists(ip, description):

    conn = sqlite3.connect("alerts.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM alerts
        WHERE ip = ?
        AND description = ?
        LIMIT 1
        """,
        (ip, description)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def save_alert(severity, ip, description):

    if alert_exists(ip, description):
        return

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


def get_alerts(severity=None, ip=None):

    conn = sqlite3.connect("alerts.db")

    cursor = conn.cursor()

    query = """
        SELECT
            timestamp,
            severity,
            ip,
            description
        FROM alerts
        WHERE 1=1
    """

    params = []

    if severity and severity != "ALL":

        query += " AND severity = ?"
        params.append(severity)

    if ip:

        query += " AND ip LIKE ?"
        params.append(f"%{ip}%")

    query += " ORDER BY id DESC"

    cursor.execute(query, params)

    alerts = cursor.fetchall()

    conn.close()

    return alerts