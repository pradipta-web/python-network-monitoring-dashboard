import sqlite3
from config import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ip_address TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER,
            status TEXT,
            latency REAL,
            packet_loss REAL,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (device_id) REFERENCES devices(id)
        )
    """)

    connection.commit()
    connection.close()


def save_monitoring_history(device_id, status, latency, packet_loss=0):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO monitoring_history
        (device_id, status, latency, packet_loss)
        VALUES (?, ?, ?, ?)
    """, (device_id, status, latency, packet_loss))

    connection.commit()
    connection.close()


def get_monitoring_history():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            monitoring_history.id,
            devices.name,
            devices.ip_address,
            monitoring_history.status,
            monitoring_history.latency,
            monitoring_history.packet_loss,
            monitoring_history.checked_at
        FROM monitoring_history
        LEFT JOIN devices
        ON monitoring_history.device_id = devices.id
        ORDER BY monitoring_history.checked_at DESC
    """)

    history = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return history